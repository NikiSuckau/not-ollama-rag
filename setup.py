from tinydb import TinyDB
import os, re, shutil, subprocess

MAIN_MODEL_DEFAULT = "deepseek-chat"
FAST_MODEL_DEFAULT = "deepseek-chat"
API_BASE_URL_DEFAULT = "https://api.deepseek.com/v1"

db = TinyDB('./config.json')
agent_table = db.table('agent')
model_table = db.table('model')

def start():
    os.environ["TOKENIZERS_PARALLELISM"] = "false" # required to run Chroma DB properly on CPU
    print("*** CONFIG TOOL")
    configAgent()
    configModel()
    print("*** CONFIG IS COMPLETE")

def configAgent():
    row = None
    if len(agent_table.all()) > 0:
        row = agent_table.all()[0]
    if row == None:
        row = {"active": True}
        agent_table.insert(row)
    if row.get("agent_type") == None:
        user_input = inputForAccepted(
            "Chatbot agent type/description:",
            lambda: input("E.g. \"a research assistant\"\n> The chatbot agent is... "),
            lambda _: print("Accept?")
        ).strip()
        row["agent_type"] = user_input
        agent_table.update(row, doc_ids=[1])
    if row.get("agent_name") == None:
        user_input = inputForAccepted(
            "Agent (chatbot) name (a single first name works best):",
            lambda: input("> Name: "),
            lambda _: print("Accept?")
        ).strip()
        row["agent_name"] = user_input
        agent_table.update(row, doc_ids=[1])
    if row.get("agent_relation") == None:
        user_input = inputForAccepted(
            "Agent relation (writen as to the agent):",
            lambda: input(f"E.g. \"your supervisor\"\n> I am... "),
            lambda _: print("Accept?")
        ).strip()
        row["agent_relation"] = user_input
        agent_table.update(row, doc_ids=[1])
    if row.get("agent_attitude") == None:
        user_input = inputForAccepted(
            "Agent attitude:",
            lambda: input(f"E.g. \"researches new topics and discusses existing research.\"\n> {row['agent_name']}... "),
            lambda _: print("Accept?")
        ).strip()
        row["agent_attitude"] = user_input
        agent_table.update(row, doc_ids=[1])
    if row.get("user_name") == None:
        user_input = inputForAccepted(
            "Your name:",
            lambda: input("> Name: "),
            lambda _: print("Accept?")
        ).strip()
        row["user_name"] = user_input
        agent_table.update(row, doc_ids=[1])
    print("Agent config is complete")

def configModel():
    row = None
    if len(model_table.all()) > 0:
        row = model_table.all()[0]
    if row == None:
        row = {"active": True}
        model_table.insert(row)
    if row.get("api_base_url") == None:
        user_input = inputForAccepted(
            "OpenAI-compatible API base URL:",
            lambda: input(f"(Empty for default '{API_BASE_URL_DEFAULT}')> API Base URL: "),
            lambda _: print("Accept?")
        ).strip()
        if user_input == "":
            user_input = API_BASE_URL_DEFAULT
        row["api_base_url"] = user_input
        model_table.update(row, doc_ids=[1])
    if row.get("api_key") == None:
        user_input = inputForAccepted(
            "API Key:",
            lambda: input(f"> API Key: "),
            lambda _: print("Accept?")
        ).strip()
        row["api_key"] = user_input
        model_table.update(row, doc_ids=[1])
    if row.get("main_model") == None:
        user_input = inputForAccepted(
            "Main model name for conversation:",
            lambda: input(f"(Empty for default '{MAIN_MODEL_DEFAULT}')> Main model: "),
            lambda _: print("Accept?")
        ).strip()
        if user_input == "":
            user_input = MAIN_MODEL_DEFAULT
        row["main_model"] = user_input
        model_table.update(row, doc_ids=[1])
    if row.get("fast_model") == None:
        user_input = inputForAccepted(
            "Fast model name for simple tasks:",
            lambda: input(f"(Empty for default '{FAST_MODEL_DEFAULT}')> Fast model: "),
            lambda _: print("Accept?")
        ).strip()
        if user_input == "":
            user_input = FAST_MODEL_DEFAULT
        row["fast_model"] = user_input
        model_table.update(row, doc_ids=[1])
    print("Model config is complete")

def flatten(list_of_dicts):
    result = {}
    for d in list_of_dicts:
        if isinstance(d, dict):
            for k, v in d.items():
                result[k] = v
        elif hasattr(d, '__dict__'):
            for attr_name in dir(d):
                if not attr_name.startswith('__') and not callable(getattr(d, attr_name)):
                    result[attr_name] = getattr(d, attr_name)
    return result

def inputForAccepted(title, generator, confirmation=None):
    isAccepted = False
    data = None
    while not isAccepted:
        print(title)
        data = generator()
        if confirmation != None:
            confirmation(data)
        isAccepted = inputAccepted()
        print()
        if not isAccepted:
            print("-----------------------------")
    return data

def inputAccepted():
    accept = input("> Accept [y/n]?")
    return re.search("y", accept, re.IGNORECASE) != None

if __name__ == "__main__":
    start()

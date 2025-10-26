import os
import yaml

# build absolute path to githelp/data/overlays
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "data", "overlays")

def load_overlay(command: str):
    fname = f"{command}.yml"
    path = os.path.join(DATA_DIR, fname)
    try:
        #try opening the file and parse the yaml to python object
        #default to {} if empty
        with open(path, "rb") as f:
            data = yaml.safe_load(f) or {}
        #expect dict at the top level
        if not isinstance(data, dict):
            return None
        #a check: if yaml includes the command key and if command doesnt match command then return none
        if data.get("command") and data["command"] != command:
            return None
        #return the parsed, validated dictionary
        return data
    #if the yaml file doesnt exist then return none
    except FileNotFoundError:
        return None
    #if any other error then return none
    except Exception:
        return None
#basically a list of command for tips
def list_overlay_names():
    #if the overlays folder doesnt exist then return empty list
    if not os.path.isdir(DATA_DIR):
        return []
    #names variable stores an empty list
    names = []
    #a for loop that iterate over single file in the overlays directory 
    for entry in os.listdir(DATA_DIR):
        #build a full path for this entry
        full_path = os.path.join(DATA_DIR, entry)
        #if the path ends with .yml then strip it and then append it
        if os.path.isfile(full_path) and entry.endswith(".yml"):
            # strip .yml
            names.append(entry[:-4])
    #sort the names to make it easier to find
    names.sort()
    #return the names
    return names

def render_overlay(d: dict) -> str:
    #line variable that stores a list of outputs
    lines = []
    #append header
    lines.append("\ngithelp tips")

    #get the summary, when to use, and example in the dictionary
    summary = d.get("summary")
    when_to_use = d.get("when_to_use")
    examples = d.get("examples")

    #summary = true then append the summary text to line list
    if summary:
        lines.append("")
        lines.append(summary)
    #when to use = true then append the item in the when to use to line list
    if when_to_use:
        lines.append("\nWhen to use")
        for item in d["when_to_use"]:
            lines.append(f" - {item}")
    #example = true then for each example(ex) in examples append to line list
    if examples:
        lines.append("\nExamples")
        for ex in d["examples"]:
            #get the cmd and say
            cmd = ex.get("cmd", "")
            say = ex.get("say", "")
            lines.append(f" $ {cmd}")
            # If say exists, indent it by 3 spaces
            if say:
                lines.append(f"   {say}")
    #append a new line at the end
    lines.append("")
    #join all lines into a single string and return it
    return "\n".join(lines)

def render_menu():
    #declare an empty list called lines
    lines = []
    #display commands
    lines.append("Commands:")
    lines.append("  - run <subcommand>   Show tips for a git subcommand")
    lines.append("  - list               List available tip pages\n")

    #list all overlays found in data/overlays
    names = list_overlay_names()
    if names:
        lines.append("Available tip pages:")
        for n in names:
            lines.append(f"  - {n}")
    else:
        lines.append("No tip pages found.")
    return "\n".join(lines)
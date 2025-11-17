import os
import yaml

#build absolute path to githelp/data/overlays
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "data", "overlays")
#master dictionary file: to /src/githelp/data/overlays/tips.yml
MASTER_FILE = os.path.join(DATA_DIR, "tips.yml")


def read_yaml(path: str):
    '''
    Read a YAML file into a Python object.

    Parameters
    ----------
    path : str
        Path to the YAML file to read.

    Returns
    -------
    dict
        Parsed YAML contents. Returns an empty dict if the file is empty
        or if any error occurs while reading/parsing.
    '''
    try:
        #r opens the file for reading in text mode, and encoding="utf-8" tells Python to decode the file's bytes 
        #as UTF-8 text into normal Python strings
        with open(path, "r", encoding="utf-8") as f:
            #convert YAML content to Python object or empty dict if file is empty
            data = yaml.safe_load(f) or {}
        #return the data of whatever was loaded
        return data
    except Exception:
        #if error occurs return empty dict
        return {}
    
def helper():

    data = read_yaml(MASTER_FILE)
    return data

def load_overlay(command: str):
    '''
    Get the tips for one git subcommand.

    This first looks in the master file tips.yml under the given
    command name (ex "pull"). If found, it returns the corresponding
    dictionary of tips.

    Parameters
    ----------
    command : str
        Name of the git subcommand whose overlay should be loaded.

    Returns
    -------
    dict or None
        The overlay dictionary for the given command, with a ``"command"`` key
        ensured, or ``None`` if no overlay is defined.
    '''
    #set data to the master dictionary file
    data = helper()
    #check to see if the master is a dict and not empty
    if isinstance(data, dict):
        #get the section for this specific command and store it in section
        section = data.get(command)
        #check if section is a dict
        if isinstance(section, dict):
            # make sure the section has a command key
            # does nothing if "command" already exists
            section.setdefault("command", command)
            #return the section
            return section


def list_overlay_names():
    '''
    List available subcommand names from tips.yml.

    Returns
    -------
    list of str
        Sorted list of subcommand names found in the master tips mapping.
    '''
    names = []
    data = helper()
    #check if data is a dict and not empty
    if not isinstance(data, dict):
        return names

    for key, value in data.items():
        if isinstance(value, dict):
            names.append(key)

    names.sort()
    return names
def render_overlay(d: dict) -> str:
    '''
    Render a single overlay dictionary into a human-readable text block.

    Parameters
    ----------
    d : dict
        Overlay dictionary containing keys such as ``"summary"``,
        ``"when_to_use"``, and ``"examples"`` (any of which may be absent).

    Returns
    -------
    str
        A formatted multi-line string 
    '''
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
    #example = true then append new line and example into line
    if examples:
        lines.append("\nExamples")
        #for each example in d["examples"]
        for ex in d["examples"]:
            #get the cmd and say
            cmd = ex.get("cmd", "")
            say = ex.get("say", "")
            lines.append(f" $ {cmd}")
            # If say exists, indent it by 3 spaces for formatting
            if say:
                lines.append(f"   {say}")
    #append a new line at the end
    lines.append("")
    #join all lines into a single string and return it
    return "\n".join(lines)

def render_menu():
    '''
    Render the main menu text for githelp.

    Returns
    -------
    str
        A formatted multi-line string describing available commands.
    '''
    #declare an empty list called lines
    lines = []
    #display commands
    lines.append("Commands:")
    lines.append("  - explain <subcommand>   Show an explaination for a git subcommand")
    lines.append("  - list                   List available tip pages\n")

    #name variable that stores the list of overlay names
    names = list_overlay_names()
    #if name is true then append the available tip pages to line list
    if names:
        lines.append("Available tip pages:")
        #for each name in names
        for n in names:
            #append each name with a dash and space before it for formatting
            lines.append(f"  - {n}")
    else:
        #if no names found append no tip pages found to line list
        lines.append("No tip pages found.")
    return "\n".join(lines)
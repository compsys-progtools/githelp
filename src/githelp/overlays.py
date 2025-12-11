import os
import yaml

#build absolute path to githelp/data/overlays
THIS_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(THIS_DIR, "data", "overlays")
#TIPS dictionary file: to /src/githelp/data/overlays/tips.yml
TIPS_FILE = os.path.join(DATA_DIR, "tips.yml")


def read_yaml(path):
    '''
    Read a YAML file into a Python object.

    Parameters
    ----------
    path
        Path to the YAML file to read.

    Returns
    -------
    dict
        Parsed YAML contents. Returns an empty dict if the file is empty
        or if any error occurs while reading/parsing.
    '''
    try:
        # opens the file for reading in text mode, and encoding="utf-8" tells Python to decode the file's bytes 
        #as UTF-8 text into normal Python strings
        with open(path, "r", encoding="utf-8") as f:
            #convert YAML content to Python object or empty dict if file is empty
            data = yaml.safe_load(f) or {}
        #return the data of whatever was loaded
        return data
    except Exception:
        #if error occurs return empty dict
        return {}

def load_overlay(command):
    '''
    Get the tips for one git subcommand.

    This first looks in the TIPS file tips.yml under the given
    command name (ex `pull`). If found, it returns the corresponding
    dictionary of tips.

    Parameters
    ----------
    command
        Name of the git subcommand
    Returns
    -------
    dict or None
        The overlay dictionary for the given command, with a ``"command"`` key
        ensured, or ``None`` if no tip is defined.
    '''
    data = read_yaml(TIPS_FILE)

    # if the YAML didn't load as a dict, bail out early
    if not isinstance(data, dict):
        return None
    # section for this specific command
    section = data.get(command)
    # if there's no entry (or it's not a dict), bail out
    if not isinstance(section, dict):
        return None
    # make sure the section has a "command" key
    section.setdefault("command", command)
    return section


def list_tips_names():
    '''
    List available subcommand names from tips.yml.

    Returns
    -------
    list of str
        Sorted list of subcommand names found in the TIPS tips mapping.
    '''
    data = read_yaml(TIPS_FILE)
    if not isinstance(data, dict):
        return []

    # just return all the keys, sorted
    return sorted(data.keys())
def render_overlay(dict):
    '''
    Render a single overlay dictionary into a human readable text block.

    Parameters
    ----------
    dict
        Overlay dictionary containing keys such as ``"summary"``,
        It has ``"when_to_use"``, and ``"examples"``.

    Returns
    -------
    str
        Using fstring to format the text block for display.
    '''
    #line variable that stores a list of outputs
    lines = []
    #append header
    lines.append("\ngithelp tips")

    #get the summary, when to use, and example in the dictionary
    summary = dict.get("summary")
    when_to_use = dict.get("when_to_use")
    examples = dict.get("examples")

    #summary = true then append the summary text to line list
    if summary:
        lines.append("")
        lines.append(summary)
    #when to use = true then append the item in the when to use to line list
    if when_to_use:
        lines.append("\nWhen to use")
        for item in dict["when_to_use"]:
            lines.append(f" - {item}")
    #example = true then append new line and example into line
    if examples:
        lines.append("\nExamples")
        #for each example in dict["examples"]
        for ex in dict["examples"]:
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
        Using fstring to format the text block for display.
    '''
    #declare an empty list called lines
    lines = []
    #display commands
    lines.append("Githelp Commands:")
    lines.append("  - explain <subcommand>   Show an explaination for a git subcommand")
    lines.append("  - list                   List available tip pages")
    lines.append("  - tips <subcommand>      Show tips.yml page for a git subcommand")
    lines.append("  - save                   High-level save: git add, commit, push")

    #name variable that stores the list of tips names
    names = list_tips_names()
    #if name is true then append the available tip pages to line list
    if names:
        lines.append("Available tips:")
        #for each name in names
        for n in names:
            #append each name with a dash and space before it for formatting
            lines.append(f"  - {n}")
    else:
        #if no names found append no tip pages found to line list
        lines.append("No tip pages found.")
    return "\n".join(lines)
# Developer Documentation

## Welcome to GitHelp

Learn Git faster, directly from your terminal, with friendly tips and optional AI-powered explanations.

---
## Description

Githelp is a command line tool designed to help CSC311 student understand and remember Git commands, while working through git. Instead of searching the web every time, you forget what `git status` or `git rebase` does, you can ask Githelp inside the terminal.

GitHelp reads from a set of tips which are stored in a YAML file and can also use an AI model (`llama2` one of Ollama model) to generate a more detail explanations when available. Whether you’re just starting with Git or brushing up on specific commands, GitHelp can help you on the fly.

With a focus on clarity, GitHelp aims to reduce frustration, support learning by doing, and make Git feel less intimidating.

---

## Installation
You can start cloning to work locally or download directly from github. 

### By clone

You can clone first
```
git clone https://github.com/compsys-progtools/githelp.git
```

and then install 
```
pip install githelp
```
(If you are using pip3)
```
pip3 install githelp
```

For development purposes, you may want to install with pip's `-e` option

```
pip install -e .
```

To update, pull and install again. 

The main use is as a CLI, for a list of all commands see the 
[CLI](cli.md) page. 

## structures

1. **CLI using Click library**  
   - Implements the `githelp` command and subcommands (`list`, `explain`, etc.).
   - Handles parsing arguments, options, and routing to the right functions.
   - [Click's library documentation](https://click.palletsprojects.com/en/stable/)

2. **`tips.yml` and the Yaml Library**  
   - A YAML file that stores tip data in a dictionary format for each Git subcommand and can be found inside the data directory.
   - Each entry contains a `summary`, `when_to_use`, and `examples`.
   - [yaml's library](https://pypi.org/project/PyYAML/)

3. **Rendering layer**  
   - Functions that take the dictionaries and convert them into readable text for the terminal (Example - `render_overlay`, `render_menu` in overlays.py).

4. **AI integration**  
   - When parsing the cmd `githelp explain <subcommand>` GitHelp calls a helper function to query the `llama2`.
   - If anything fails (Ollama not installed, model missing, network error), GitHelp falls back to the standard tips(tips.yml).
   - The model prompt can be change to developer's preference. 
   - The model can also be change to developer's preference, however the current default is set to `llama2`

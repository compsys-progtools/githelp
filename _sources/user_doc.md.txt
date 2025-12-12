# User Documentation

## Welcome to GitHelp

Learn Git faster, directly from your terminal, with friendly tips and optional AI powered explanations.

---
## Description

Githelp is a command line tool designed to help CSC311 student understand and remember Git commands, while working through git. Instead of searching the web every time, you forget what `git status` or `git rebase` does, you can ask Githelp inside the terminal.

GitHelp reads from a set of tips which are stored in a YAML file and can also use an AI model (`llama2` one of Ollama model) to generate a more detail explanations when available. Whether you’re just starting with Git or brushing up on specific commands, GitHelp can help you on the fly.

With a focus on clarity, GitHelp aims to reduce frustration, support learning by doing, and make Git feel less intimidating.

---

## Key Features

**<u>Tips</u>**  
Get concise explanations for common Git subcommands such as `add`, `status`, `commit`, `pull`, and more. Each tip includes:
- A summary of what the command does  
- When you would typically use it  
- Example command lines you can copy and adapt  

**<u>AI-Powered Explanations</u>**  
Ask GitHelp to explain a Git subcommand using the `llama2` model
- Requires [Ollama](https://ollama.com/download) to be installed

**<u>High Level Save Command</u>**  
Use `githelp save` to save work flow under this single command
- Stages your modified files for commit  
- Prompts you for a clear, meaningful commit message  
- Runs `git add`, `git commit`, and `git push` for you  
- If it encounter an error when pushing it will automatically sets an upstream branch

Perfect for learners who want to do the right Git steps without memorizing every individual command.
## Installation
You can install after cloning to work locally or directly from github. 

### By Git Clone

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

## Usage 

The main use is as a CLI, for a list of all commands see the 
[CLI](cli.md) page. 
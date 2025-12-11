import subprocess

def ask_ollama(git_output, mode="explain"):
    """Ask an ollama model to explain captured git output.

    Parameters
    ----------
    git_output
        The stdout text from a git command (ex `git status`).
    model
        Name of the ollama model or modelfile to use, by default "githelp".

    Returns
    -------
    str
        Explanation text from ollama, or an error message if something fails.
    """
    model = "llama2"
    #prompt tuned for the LLM model
    if mode == "save":
        #short, one phrase summary
        prompt = (
            "you are a git tutor for the CSC 311 course.\n"
            "explain very briefly what this git command does.\n"
            "respond in ONE short phrase, at most 20 characters.\n"
            "do NOT include examples, extra tips, or newlines.\n"
            f"{git_output}\n"
        )
    else:
        #default more detailed explanation for `githelp explain`.
        prompt = (
            "you are a git tutor for the CSC 311 course.\n"
            "explain the following git output to a beginner.\n"
            "please explain in simple terms and keep it under 100 words.\n"
            "please provide examples on how to use the commands.\n"
            "if they struggle with git commands, provide tips and be detailed.\n"
            "if they come across an error, help guide them to fix it.\n"
            "if they still do not understand after several tries, show a clear answer.\n"
            f"{git_output}\n"
        )


    try:
        #this here runs the ollama command with the given model
        completed = subprocess.run( 
             #this is the command being run -> ollama run <model>
            ["ollama", "run", model],
            input = prompt,
            #tell the subprocess that it is working with text
            text = True,
            #use UTF-8 to turn strings into bytes and bytes into strings
            encoding = "utf-8",
            #how to handle encoding errors that can't be encoded that it doesnt crash
            errors = "replace",
            #tell it to capture stdout and stderr to variables
            stdout  = subprocess.PIPE,
            stderr = subprocess.PIPE,
            #raise an error if the command fails
            check = True,
        )
    except FileNotFoundError:
        #if ollama is not installed
        return (
            "githelp: `ollama` command not found.\n"
            "To use this feature, install Ollama from https://ollama.com/download "
        )
    #this captures errors from the ollama command itself
    except subprocess.CalledProcessError as exc:
        #if ollama returns an error
        err = exc.stderr or str(exc)
        return f"githelp: ollama returned an error:\n{err}"
    #if everything worked,
    return completed.stdout
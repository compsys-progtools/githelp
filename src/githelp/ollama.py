import subprocess

def ask_ollama(git_output):
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
    prompt = (
        "you are a git tutor for the CSC 311 course.\n"
        "explain the following git output to a beginner.\n"
        "please explain in simple terms and kept it under 100 words\n"
        "please provide examples on how to use the commands\n"
        "if they stuggle with git command please provide some more tips and try to be more detailed\n"
        "if they come across an error please help guide them to fix it\n"
        "if they did not get it after the first 4 tries please provide them with the answer\n"
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
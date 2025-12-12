import click
import subprocess
from .overlays import load_overlay, render_overlay, render_menu
from .ollama import ask_ollama

@click.group(
    help="githelp terminal first Git helper.",
    invoke_without_command = True,
    add_help_option = False,
)
@click.option("-h", "--help", "show_help", is_flag = True, help = "Provides option menu")
@click.pass_context
def githelp_cli(context, show_help):
    if show_help or context.invoked_subcommand is None:
        click.echo(context.get_help())
        click.echo()
        click.echo(render_menu())
        if context.invoked_subcommand is None:
            context.exit(0)

@githelp_cli.command(help = "List of available githelp tip pages.")
def list():
    '''List all available githelp tip.'''
    click.echo(render_menu())

@githelp_cli.command(
    name = "explain",
    help = "Explain a git subcommand. Uses ollama if available, otherwise tips.yml.",
)
@click.argument("cmd")

def explain_cmd(cmd):
    """
    Explain a git subcommand

    - Tries to use ollama (default model - llama2) to explain git command.
    - If ollama is not installed or returns an error, falls back to tips.yml.
    """
    #load tips.yml entry for this subcommand
    tips = load_overlay(cmd)
    if not tips:
        click.echo(f"githelp tips\n\nNo tips found for '{cmd}'.")
        return

    #base explanation text from tips.yml
    rendered = render_overlay(tips)

    #try to use ollama first
    explanation = ask_ollama(rendered)
    #otherwise, show ONLY the AI explanation
    click.echo(explanation)

@githelp_cli.command(
    name = "tips",
    help = "Show the tips.yml page for a git subcommand.",
)
@click.argument("cmd")
def tips_cmd(cmd):
    """
    Show tips.yml content for a specific git subcommand.

    Examples
    --------
    - githelp tips add
    - githelp tips status
    - githelp tips branch
    """
    tips = load_overlay(cmd)
    if tips:
        click.echo(render_overlay(tips))
    else:
        click.echo(f"githelp tips\n\nNo tips found for '{cmd}'.")

def run_git_command(args):
    """
    Run a git command and print its output.

    Parameters
    ----------
    args
        args = ["add", "."]             -> runs `git add .`
        args = ["commit", "-m", "msg"]  -> runs `git commit -m "msg"`
        args = ["push"]                 -> runs `git push`
        Special behavior
    ----------------
    - If `git push` fails because there is no upstream branch set,
      this function will try to fix it by running:
          git push --set-upstream origin <current-branch>
      and will then return True if that succeeds.

    Parameters
    ----------
    args : list[str]
        List of arguments to pass after the `git` command.

    Returns
    -------
    bool
        True if the git command or its automatic fix succeeded,
        False if it failed.
    """
    try:
        completed = subprocess.run(
            ["git"] + args,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True,
        )
        if completed.stdout:
            click.echo(completed.stdout)
        return True
    except subprocess.CalledProcessError as exc:
        output = exc.stdout or exc.stderr or str(exc)
        text = output or ""

        #special case - handle no upstream branch error for git push
        if args == ["push"] and "has no upstream branch" in text:
            click.echo("githelp save - detected missing upstream, setting it up now...")

            #figures out current branch name
            try:
                branch_proc = subprocess.run(
                    ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    check=True,
                )
                branch = branch_proc.stdout.strip()
            except subprocess.CalledProcessError:
                #show original error and bail
                click.echo(output)
                click.echo("githelp save - sorry could not determine current branch name.")
                return False

            #this runs git push --set-upstream origin <branch>
            try:
                fix_proc = subprocess.run(
                    ["git", "push", "--set-upstream", "origin", branch],
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=True,
                )
                if fix_proc.stdout:
                    click.echo(fix_proc.stdout)
                return True
            except subprocess.CalledProcessError as exc2:
                #if fix also fails, show errors
                out2 = exc2.stdout or exc2.stderr or str(exc2)
                click.echo(output)
                click.echo(out2)
                return False

        #default behavior just show the error
        click.echo(output)
        return False


def ai_explain_step(subcommand):
    """
    Use ollama to briefly explain one git subcommand.

    This uses the short "save" mode prompt so that the response
    is a very small phrase suitable for inline display after
    each part of the save steps.
    """
    rendered = render_overlay(load_overlay(subcommand))
    explanation = ask_ollama(rendered, mode="save")
    #otherwise show llama2 explanation
    click.echo(explanation.strip())

@githelp_cli.command(
    name="save",
    help="High level save - run git add, commit, and push, then ollama2 explain each step.",
)
@click.option(
    "--message",
    help='Commit message to use for git commit. If omitted, you will be prompted.',
)
def save_cmd(message):
    """
    Run git add, commit, and push as one high level "save" step.

    Behind the scenes this does:

    githelp save
    this will do the follow:
    - it will auto run ``git add .`` and then AI explain git add
    - it will auto run ``git commit -m "<message>"`` and then AI explain git commit
    - it will auto run ``git push`` and then AI explain git push
    """
    click.echo("githelp save will run the following git commands in this repository:")
    click.echo("  1. git add .")
    click.echo('  2. git commit -m "<message>"')
    click.echo("  3. git push")
    #confirmation before proceeding
    confirm = click.confirm("Are you sure you want to run these commands now?", default=False)
    if not confirm:
        click.echo("githelp save: cancelled by user.")
        return

    click.echo("githelp save: running high-level save (add, commit, push).")

    #step 1 -> git add .
    click.echo()
    click.echo("git add .")
    run_git_command(["add", "."])
    ai_explain_step("add")
    click.echo()

    #step 2 -> git commit -m "<message>"
    click.echo()
    #try to run message from command line argument where user inputs it or get a default message
    if not message:
        message = click.prompt("Commit message", default="save changes")
    
    click.echo(f'git commit -m "{message}"')
    #try to run git commit with the given message and if it fails, stop, show error and exit
    if not run_git_command(["commit", "-m", message]):
        click.echo("githelp save: stopping because 'git commit' returned an error.")
        return
    ai_explain_step("commit")
    click.echo()

    #step 3 -> git push 
    click.echo("git push")
    # Try to run git push.
    # If it fails, show an error and stop. run_git_command may auto handle upstream issue.
    if not run_git_command(["push"]):
        click.echo("githelp save: stopping because 'git push' returned an error.")
        return

    ai_explain_step("push")
    click.echo()
    click.echo("githelp save: finished.")
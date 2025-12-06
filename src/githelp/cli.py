import click
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
    """Explain a git subcommand

    - Tries to use ollama (default model - llama2) to explain git command.
    - If ollama is not installed or returns an error, falls back to tips.yml.
    """
    #load tips.yml entry for this subcommand
    tips = load_overlay(cmd)
    if not tips:
        click.echo(f"githelp tips\n\nNo tips found for '{cmd}'.")
        return

    # Base explanation text from tips.yml
    rendered = render_overlay(tips)

    # Try to use ollama first
    explanation = ask_ollama(rendered)

    # If ollama isn't available or errors then show tips.yml
    if explanation.startswith("githelp: `ollama` command not found.") or \
       explanation.startswith("githelp: ollama returned an error:"):
        #show error message to user that way they know why AI explanation is not available
        click.echo(explanation)
        click.echo()
        # Just show the tips.yml explanation
        click.echo(rendered)
        return

    #otherwise, show ONLY the AI explanation
    click.echo(explanation)

@githelp_cli.command(
    name = "tips",
    help = "Show the tips.yml page for a git subcommand.",
)
@click.argument("cmd")
def tips_cmd(cmd):
    """Show tips.yml content for a specific git subcommand.

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
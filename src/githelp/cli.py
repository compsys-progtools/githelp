import click
from .overlays import load_overlay, render_overlay, render_menu

@click.group(
    help="githelp terminal first Git helper.",
    invoke_without_command=True,
    add_help_option=False,
)
@click.option("-h", "--help", "show_help", is_flag=True, help="Provides option menu")
@click.pass_context
def githelp_cli(context, show_help):
    if show_help or context.invoked_subcommand is None:
        click.echo(context.get_help())
        click.echo()
        click.echo(render_menu())
        if context.invoked_subcommand is None:
            context.exit(0)

@githelp_cli.command(name="list", help="List of available githelp tip pages.")
def list_cmd():
    '''List all available githelp tip.'''
    click.echo(render_menu())

@githelp_cli.command(name="explain", help="Show githelp overlay tips for a git subcommand.")
@click.argument("cmd")
def explain_cmd(cmd):
    '''Show tips for a specific git subcommand'''
    tips = load_overlay(cmd)
    if tips:
        click.echo(render_overlay(tips))
    else:
        click.echo(f"githelp tips\n\nNo tips found for '{cmd}'.")
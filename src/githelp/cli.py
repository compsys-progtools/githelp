import click
from .greeter import make_greeting

#declare the click command
#the text in help show up in the githelp --help
@click.command(help="Say hello from githelp.")
@click.option("--name", "-n", default="World", show_default=False, help="Who to greet.")
#here there is a boolean flag pair --shout/--no-shout"
@click.option("--shout/--no-shout", default=False, show_default=False, help="End with an exclamation mark.")
#click auto parse the value
def githelp_cli(name: str, shout: bool) -> None:
    click.echo(make_greeting(name, shout))
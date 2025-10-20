#import the click library for the building cli interfaces
import click
#import the inner function that actually builds the greeting text
#keynote ".greater" is a relative import not an absolute.
from .greeter import make_greeting

#declare the click command
#the text in help show up in the githelp --help
@click.command(help="Say hello from githelp.")
#option "--name is define" and "-n" for short 
#default= World if user didnt provide a name
#show default flag is set to false so it doesnt display in option
@click.option("--name", "-n", default="World", show_default=False, help="Who to greet.")
#here there is a boolean flag pair --shout/--no-shout"
@click.option("--shout/--no-shout", default=False, show_default=False, help="End with an exclamation mark.")
#click auto parse the value
def main(name: str, shout: bool) -> None:
     #call the inner function to build the message, then print it to stdout
    click.echo(make_greeting(name, shout))
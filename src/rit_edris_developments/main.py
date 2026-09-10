import typer

from rit_edris_developments.commands import *

app = typer.Typer()
app.add_typer(stack_app, name="stack")
app.add_typer(terraform_app, name="terraform")

if __name__ == "__main__":
    app()

import logging
import sys
import typer

import rit_edris_developments.commands

app = typer.Typer()
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)

for nom in rit_edris_developments.commands.__all__:
    name = nom.replace("_app", "")
    app.add_typer(getattr(rit_edris_developments.commands, nom), name=name)

if __name__ == "__main__":
    app()

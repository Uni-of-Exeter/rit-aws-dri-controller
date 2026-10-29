import logging
import sys
import typer

import rit_aws_dri_controller.commands

app = typer.Typer()
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logging.getLogger("botocore").setLevel(logging.INFO)
logging.getLogger("boto3").setLevel(logging.INFO)

for nom in rit_aws_dri_controller.commands.__all__:
    name = nom.replace("_app", "")
    app.add_typer(getattr(rit_aws_dri_controller.commands, nom), name=name)

if __name__ == "__main__":
    app()

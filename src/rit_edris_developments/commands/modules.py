
import typer

from rit_edris_developments.modules.generator import ModuleGenerator

generator = ModuleGenerator()


def create(
    module_type: str,
    name: str,
    environment: str = "dev",
):

    path = generator.create_module(
        module_type=module_type,
        name=name,
        environment=environment,
    )

    typer.echo(
        f"Created module: {path}"
    )
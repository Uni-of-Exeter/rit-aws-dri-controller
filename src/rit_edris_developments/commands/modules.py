import typer

from rit_edris_developments.modules.generator import ModuleGenerator

module_app = typer.Typer()
generator = ModuleGenerator()


@module_app.command()
def create(
    module_type: str,
    name: str,
    environment: str = "development",
):

    path = generator.create_module(
        module_type=module_type,
        name=name,
        environment=environment,
    )

    typer.echo(
        f"Created module: {path}"
    )
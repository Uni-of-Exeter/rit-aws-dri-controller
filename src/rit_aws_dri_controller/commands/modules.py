import typer

from rit_aws_dri_controller.modules.generator import ModuleGenerator

module_app = typer.Typer()
generator = ModuleGenerator()


@module_app.command()
def create(
    name: str,
    module_type: str = "general",
    environment: str = "development",
):
    path = generator.create_module(
        name=name,
        module_type=module_type,
        environment=environment,
    )

    typer.echo(
        f"Created module: {path}"
    )
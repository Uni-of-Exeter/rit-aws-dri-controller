from typing import Union
import typer

from rit_aws_dri_controller.modules.generator import ModuleGenerator

module_app = typer.Typer()
generator = ModuleGenerator()


@module_app.command(
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True),
    help="Create a new module with arbitrary parameters mapped onto environment parameters",
)
def create(
    name: str,
    module_template: str = "general",
    param_environment: str = "dev",
):
    path = generator.create_module(
        name=name,
        module_template=module_template,
        param_environment=param_environment,
    )

    typer.echo(f"Created module: {path}")
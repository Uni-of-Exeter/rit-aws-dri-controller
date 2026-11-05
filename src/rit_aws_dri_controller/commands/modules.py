import re

import typer

from rit_aws_dri_controller.modules.generator import ModuleGenerator

module_app = typer.Typer()
generator = ModuleGenerator()


@module_app.command(
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True),
)
def create(
    name: str,
    ctx: typer.Context,
    module_template: str = "general",
    param_environment: str = "dev",
):
    """
    Create a new module with arbitrary parameters mapped onto environment parameters

    name: Name of the module
    module_template: Name of the module template to generate from
    param_environment: Name of the environment to use for this module

    All additional arguments are mapped as additional parameters into the variables of the module being
    generated. e.g. [[command]] --addition_param 1.2.3 --some_named_param t3.badmovie

    """
    param_kwargs = dict(zip(
        [re.sub(r"^--", "", el) for el in ctx.args[::2]],
        ctx.args[1::2]
    ))

    path = generator.create_module(
        name=name,
        module_template=module_template,
        param_environment=param_environment,
        **param_kwargs
    )

    typer.echo(f"Created module: {path}")
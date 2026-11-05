import os.path
import re

import typer
import yaml

from rit_aws_dri_controller.stacks.manager import StackManager
from rit_aws_dri_controller.stacks.renderer import StackRenderer

stack_app = typer.Typer()
manager = StackManager()
renderer = StackRenderer()

@stack_app.command()
def create(name: str):
    manager.create(name)
    renderer.render(name)

@stack_app.command(
    context_settings=dict(
        allow_extra_args=True,
        ignore_unknown_options=True),
)
def add(stack: str,
        module: str,
        module_type: str,
        ctx: typer.Context):
    param_kwargs = dict(zip(
        [re.sub(r"^--", "", el) for el in ctx.args[::2]],
        ctx.args[1::2]
    ))

    manager.add_module(stack, module, module_type, param_kwargs)
    renderer.render(stack)

@stack_app.command('list')
def list_stacks():
    for s in manager.stacks_dir.iterdir():
        if os.path.isdir(s):
            print(s.name)

@stack_app.command()
def show(name: str):
    stack = manager.load(name)

    typer.echo(
        yaml.dump(
            stack,
            sort_keys=False,
        )
    )
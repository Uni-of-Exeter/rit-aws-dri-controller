import os.path

import typer
import yaml

from rit_edris_developments.stacks.manager import StackManager
from rit_edris_developments.stacks.renderer import StackRenderer

stack_app = typer.Typer()
manager = StackManager()
renderer = StackRenderer()

@stack_app.command()
def create(name: str):
    manager.create(name)
    renderer.render(name)

@stack_app.command()
def add(stack: str,
        module: str,
        module_type: str):
    manager.add_module(stack, module, module_type)
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
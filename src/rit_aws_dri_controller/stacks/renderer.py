import os
from pathlib import Path

import yaml

from jinja2 import (
    Environment,
    FileSystemLoader,
)

class StackRenderer:
    def __init__(self,
                 stacks_dir: os.PathLike = 'terraform/stacks',
                 templates_dir: os.PathLike = 'terraform/templates/stacks'):
        self.stacks_dir = Path(stacks_dir)
        self.templates_dir = Path(templates_dir)

    def render(self, stack_name: str):
        stack_dir = self.stacks_dir / stack_name
        stack = yaml.safe_load((stack_dir / 'stack.yaml').read_text())

        loader = FileSystemLoader(str(self.templates_dir))
        env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        context = dict(
            stack=stack
        )
        for template_file in self.templates_dir.glob("*"):
            template = env.get_template(template_file.name)
            rendered = template.render(**context)
            (stack_dir / template_file.name).write_text(rendered)
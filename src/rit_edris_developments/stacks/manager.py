import os
from pathlib import Path

import yaml

from rit_edris_developments.stacks.models import Stack

class StackManager:
    def __init__(self, stacks_dir: os.PathLike = 'terraform/deployments'):
        self.stacks_dir = Path(stacks_dir)

    def create(self, name: str):
        d = self.stacks_dir / name
        d.mkdir(parents = True, exist_ok = True)
        (d / 'stack.yaml').write_text(
            yaml.safe_dump({'name': name, 'modules': []}))

    def load(self, name: str):
        return yaml.safe_load((self.stacks_dir / name / 'stack.yaml').read_text())

    def save(self, stack: Stack):
        (self.stacks_dir / stack.name / 'stack.yaml').write_text(yaml.safe_dump(stack))

    def add_module(self,
                   stack_name: str,
                   module_name: str,
                   module_type: str):
        s = self.load(stack_name)
        s['modules'].append({'name': module_name, 'type': module_type})

        # TODO: parse metadata from the module, add in the necessary variables
        # TODO: add and parse metadata for modules, adding outputs of use

        self.save(s)

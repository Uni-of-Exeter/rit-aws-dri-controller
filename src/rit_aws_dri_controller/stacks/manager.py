import logging
import os
from pathlib import Path

import yaml

from rit_aws_dri_controller.stacks.models import Stack

class StackManager:
    def __init__(self, stacks_dir: os.PathLike = 'terraform/stacks'):
        self.stacks_dir = Path(stacks_dir)

    def create(self, name: str):
        d = self.stacks_dir / name
        d.mkdir(parents = True, exist_ok = True)
        (d / 'stack.yaml').write_text(
            yaml.safe_dump({'name': name, 'modules': []}))
        logging.info(f"Defined {name} at {d}/stack.yaml")

    def load(self, name: str):
        stack_config_fn = self.stacks_dir / name / 'stack.yaml'
        stack_config = yaml.safe_load((self.stacks_dir / name / 'stack.yaml').read_text())
        logging.info(f"Loaded config from {stack_config_fn}")
        return stack_config

    def save(self, stack: Stack):
        stack_config_fn = self.stacks_dir / stack['name'] / 'stack.yaml'
        stack_config_fn.write_text(yaml.safe_dump(stack))
        logging.info(f"Saved {stack_config_fn}")

    def add_module(self,
                   stack_name: str,
                   module_name: str,
                   module_type: str):
        s = self.load(stack_name)

        # TODO: deduplicate naming
        s['modules'].append({'name': module_name, 'type': module_type})
        logging.info(f"Module {module_name} added to stack {s['name']}")
        # TODO: parse metadata from the module, add in the necessary variables
        # TODO: add and parse metadata for modules, adding outputs of use

        self.save(s)

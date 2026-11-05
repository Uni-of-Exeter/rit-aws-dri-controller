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
                   resource_name: str,
                   module_type: str,
                   params: dict):
        stack = self.load(stack_name)

        if resource_name in [m["name"] for m in stack['modules']]:
            raise RuntimeError(f"Resource {resource_name} already exists")

        module_spec = {
            'name': resource_name,
            'type': module_type,
            'params': {}
        }
        for k in ["aws_region", "project_name", "environment"]:
            module_spec["params"][k] = f"var.{k}"

        for k, v in params.items():
            module_spec["params"][k] = v if v.startswith("var.") else f"\"{v}\""

        stack['modules'].append(module_spec)
        logging.info(f"Module {resource_name} added to stack {stack['name']}")

        self.save(stack)

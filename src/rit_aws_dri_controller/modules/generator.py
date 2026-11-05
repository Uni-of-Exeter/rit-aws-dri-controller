import glob
import logging
import os
import pathlib

from pathlib import Path
from typing import Union

import tomllib
import yaml

from jinja2 import (
    Environment,
    FileSystemLoader,
)


class ModuleGenerator:
    """
    Creates Terraform modules from predefined Jinja2 templates.
    """

    def __init__(
        self,
        # TODO: template_root got a little messy, clean it up
        template_root="terraform/templates",
        implementation_root="terraform/modules/implementations",
    ):
        self.template_root = Path(template_root)
        self.implementation_root = Path(implementation_root)

    def create_module(
        self,
        module_template: str,
        name: str,
        param_environment: Union[str, None],
        **kwargs,
    ) -> Path:
        self._validate_module_type(module_template)
        target_dir = self.implementation_root / name

        if target_dir.exists():
            raise ValueError(f"Module already exists: {name}")

        loader = FileSystemLoader(self.template_root)
        env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        context = {
            "name": name,
            "source_template": module_template,
        }

        param_dict = dict()
        if param_environment is not None:
            template = env.get_template(f"environments/{param_environment}/terraform.tfvars")
            param_data = tomllib.loads(template.render(**context))
            param_dict.update(param_data)
        param_dict.update(kwargs)
        # This becomes the parameters and defaults dictionary for the module
        # with mappings specified in the stack add command
        context["parameters"] = param_dict

        target_dir.mkdir(parents=True, exist_ok=False)
        for template_file in pathlib.Path(f"modules/{module_template}").glob("*.*"):
            template = env.get_template(template_file.name)
            rendered = template.render(**context)
            (target_dir / template_file).write_text(rendered)

        self._write_manifest(context, target_dir)

        return target_dir

    def _validate_module_type(
        self,
        module_type: str,
    ):
        valid_types = [os.path.basename(directory)
                       for directory in os.listdir(self.template_root / "modules")
                       if os.path.isdir(self.template_root / "modules" / directory)]
        logging.debug(f"Got {len(valid_types)} valid types: {", ".join(valid_types)}")

        if module_type not in valid_types:
            raise ValueError(f"Unsupported module type: {module_type}")

    def _write_manifest(
        self,
        context: dict,
        target_dir: pathlib.Path,
    ):
        manifest = {
            "name": context["name"],
            "type": context["type"],
            "environment": context["environment"],
            "parameters": {
                k: v for k, v in context.items() if k not in [
                    "name",
                    "type",
                    "environment",
                ]
            },
        }

        with open(target_dir / "module.yaml", "w") as handle:
            yaml.safe_dump(
                manifest,
                handle,
                sort_keys=False,
            )
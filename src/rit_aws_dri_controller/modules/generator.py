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
        environment_template_root="terraform/templates/environments",
        module_template_root="terraform/templates/modules",
        implementation_root="terraform/modules/implementations",
    ):
        self.tmpl_env_root = Path(environment_template_root)
        self.tmpl_module_root = Path(module_template_root)
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
            logging.warning(f"Module already exists: {name}, only generating missing files")

        env = Environment(
            loader= FileSystemLoader(self.tmpl_env_root),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        context = {
            "name": name,
            "source_template": module_template,
        }

        param_dict = dict()
        if param_environment is not None:
            template_name = os.path.join(param_environment, "terraform.tfvars")
            template = env.get_template(template_name)
            param_data = tomllib.loads(template.render(**context))
            param_dict.update(param_data)
        param_dict.update(kwargs)
        # This becomes the parameters and defaults dictionary for the module
        # with mappings specified in the stack add command
        param_dict["module_name"] = context["name"]
        context["parameters"] = param_dict

        env = Environment(
            loader= FileSystemLoader(self.tmpl_module_root),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        target_dir.mkdir(parents=True, exist_ok=False)
        logging.info(pathlib.Path(f"modules/{module_template}"))
        for template_file in (self.tmpl_module_root / module_template).glob("*.tf"):
            template = env.get_template(os.path.join(module_template, template_file.name))
            rendered = template.render(context=context)
            target_filename = (target_dir / template_file.name)
            if not os.path.exists(target_filename):
                logging.debug(f"Generating {target_filename}")
                target_filename.write_text(rendered)
            else:
                logging.info(f"Skipped {target_filename} as already exists")

        self._write_manifest(context, target_dir)

        return target_dir

    def _validate_module_type(
        self,
        module_type: str,
    ):
        valid_types = [os.path.basename(directory)
                       for directory in os.listdir(self.tmpl_module_root)
                       if os.path.isdir(self.tmpl_module_root / directory)]
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
            "source_template": context["source_template"],
            "parameters": list(context["parameters"].keys()) + ["tags"]
        }

        with open(target_dir / "module.yaml", "w") as handle:
            yaml.safe_dump(
                manifest,
                handle,
                sort_keys=False,
            )
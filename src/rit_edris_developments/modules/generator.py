from pathlib import Path

import yaml

from jinja2 import (
    Environment,
    FileSystemLoader,
)


class ModuleGenerator:
    """
    Creates Terraform modules from
    predefined Jinja2 templates.
    """

    def __init__(
        self,
        template_root="terraform/modules/templates",
        implementation_root="terraform/modules/implementations",
    ):
        self.template_root = Path(template_root)
        self.implementation_root = Path(
            implementation_root
        )

    def create_module(
        self,
        module_type: str,
        name: str,
        environment: str = "dev",
        **kwargs,
    ) -> Path:

        self._validate_module_type(
            module_type
        )

        source_dir = (
            self.template_root /
            module_type
        )

        target_dir = (
            self.implementation_root /
            module_type /
            name
        )

        if target_dir.exists():
            raise ValueError(
                f"Module already exists: {name}"
            )

        target_dir.mkdir(
            parents=True,
            exist_ok=False,
        )

        context = {
            "name": name,
            "type": module_type,
            "environment": environment,
            **kwargs,
        }

        loader = FileSystemLoader(
            str(source_dir)
        )

        env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        for template_file in source_dir.glob(
            "*.j2"
        ):

            output_name = template_file.name.replace(
                ".j2",
                "",
            )

            template = env.get_template(
                template_file.name
            )

            rendered = template.render(
                **context
            )

            (
                target_dir / output_name
            ).write_text(rendered)

        self._write_manifest(
            target_dir,
            context,
        )

        return target_dir

    def _validate_module_type(
        self,
        module_type: str,
    ):

        valid_types = {
            "data",
            "compute",
            "application",
        }

        if module_type not in valid_types:
            raise ValueError(
                f"Unsupported module type: "
                f"{module_type}"
            )

    def _write_manifest(
        self,
        target_dir: Path,
        context: dict,
    ):

        manifest = {
            "name": context["name"],
            "type": context["type"],
            "environment": context[
                "environment"
            ],
            "parameters": {
                k: v
                for k, v
                in context.items()
                if k
                not in {
                    "name",
                    "type",
                    "environment",
                }
            },
        }

        with open(
            target_dir / "module.yaml",
            "w",
        ) as handle:
            yaml.safe_dump(
                manifest,
                handle,
                sort_keys=False,
            )
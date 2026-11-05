import logging
import os
from pathlib import Path

import shlex
import subprocess as sp

from rit_aws_dri_controller.terraform.backend import BackendManager

from jinja2 import (
    Environment,
    FileSystemLoader,
)

class EnvironmentDeployer:
    def __init__(self,
                 stack: str,
                 environment: str,
                 region: str,
                 profile: str):
        self.stack = stack
        self.environment = environment
        self.region = region
        self.profile = profile

        self.bucket_name = f"uoe-rit-{self.stack}-{self.environment}-stack-tfstate"
        self.wd = Path("terraform/stacks") / self.stack
        self.tfvars = self.wd / f"{self.environment}.tfvars"

        backend = BackendManager(
            bucket_name=f"{self.bucket_name}",
            region=self.region,
            profile=self.profile
        )
        backend.ensure_backend()
        self.config_path = os.path.basename(backend.write_configuration(self.wd))

    def write_variables(self):
        loader = FileSystemLoader(os.path.join("terraform", "templates", "environments"))
        env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        context = dict(
            stack=self.stack,
            environment=self.environment,
        )
        template = env.get_template(os.path.join(self.environment, "terraform.tfvars"))
        rendered = template.render(**context)
        (self.wd / f"{self.environment}.tfvars").write_text(rendered)
        # TODO: default variables from each module implementation can be added via jinja, hence it's use!

    def plan(self):
        self.write_variables()

        try:
            sp.run(shlex.split(f"terraform init -backend-config={self.config_path}"), cwd=self.wd, check=True)
            sp.run(shlex.split(f"terraform plan -var-file={str(self.tfvars)}"), cwd=self.wd, check=True)
        except sp.CalledProcessError as e:
            logging.warning("Failed to run plan successfully, review the terraform warning")

    def deploy(self):
        try:
            sp.run(shlex.split(f"terraform init -backend-config={self.config_path}"), cwd=self.wd, check=True)
            sp.run(shlex.split(f"terraform deploy -var-file={str(self.tfvars)}"), cwd=self.wd, check=True)
        except sp.CalledProcessError as e:
            raise RuntimeError("Failed to run deployment successfully, review the terraform warning")

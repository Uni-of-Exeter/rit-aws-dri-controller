import logging
from pathlib import Path

import shlex
import subprocess as sp

import typer

from rit_aws_dri_controller.terraform.backend import BackendManager

"""
# TODO: remove redundancy
"""

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

        self.wd = Path("terraform/stacks") / self.stack
        self.tfvars = self.wd / f"{self.environment}.tfvars"

        self.init()

    def init(self):
        backend = BackendManager(
            bucket_name=f"uoe-rit-{self.stack}-{self.environment}-stack-tfstate",
            region=self.region,
            profile=self.profile
        )

        backend.ensure_backend()

    def plan(self):
        try:
            sp.run(shlex.split("terraform init"), cwd=self.wd, check=True)
            sp.run(shlex.split(f"terraform plan -var-file={str(self.tfvars)}"), cwd=self.wd, check=True)
        except sp.CalledProcessError as e:
            logging.warning("Failed to run plan successfully, review the terraform warning")

    def deploy(self):
        try:
            sp.run(shlex.split("terraform init"), cwd=self.wd, check=True)
            sp.run(shlex.split(f"terraform deploy -var-file={str(self.tfvars)}"), cwd=self.wd, check=True)
        except sp.CalledProcessError as e:
            raise RuntimeError("Failed to run deployment successfully, review the terraform warning")

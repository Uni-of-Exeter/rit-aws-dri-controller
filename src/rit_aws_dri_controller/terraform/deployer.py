import logging
from pathlib import Path

import shlex
import subprocess as sp

from rit_aws_dri_controller.terraform.backend import BackendManager


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
        self.config_path = backend.write_configuration(self.wd)

    def plan(self):
        try:
            sp.run(shlex.split(f"terraform init -backend-config={self.config_path}"), cwd=self.wd, check=True)
            sp.run(shlex.split(f"terraform plan -backend-config={self.config_path} -var-file={str(self.tfvars)}"), cwd=self.wd, check=True)
        except sp.CalledProcessError as e:
            logging.warning("Failed to run plan successfully, review the terraform warning")

    def deploy(self):
        try:
            sp.run(shlex.split(f"terraform init -backend-config={self.config_path}"), cwd=self.wd, check=True)
            sp.run(shlex.split(f"terraform deploy -backend-config={self.config_path} -var-file={str(self.tfvars)}"), cwd=self.wd, check=True)
        except sp.CalledProcessError as e:
            raise RuntimeError("Failed to run deployment successfully, review the terraform warning")

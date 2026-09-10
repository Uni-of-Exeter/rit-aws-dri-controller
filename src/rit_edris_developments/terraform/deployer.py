from pathlib import Path

import subprocess as sp


class EnvironmentDeployer:
    def deploy(self, stack: str, environment: str):
        wd = Path("terraform/deployments") / stack
        tfvars = Path("terraform/environments") / environment / "terraform.tfvars"

        sp.run(
            ["terraform", "init"],
            cwd = wd,
            check = True)
        sp.run(
            ["terraform", "plan",
                  "-var-file", str(tfvars), "-auto-approve"],
            cwd = wd,
            check = True)
        #sp.run(
        #    ["terraform", "apply",
        #          "-var-file", str(tfvars), "-auto-approve"],
        #    cwd = wd,
        #    check = True)

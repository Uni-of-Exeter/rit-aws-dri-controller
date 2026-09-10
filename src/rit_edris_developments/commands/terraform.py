import typer

from rit_edris_developments.terraform.backend import BackendManager
from rit_edris_developments.terraform.deployer import EnvironmentDeployer

terraform_app = typer.Typer()

@terraform_app.command()
def deploy(
    stack: str,
    environment: str = "dev",
    region: str = "eu-west-2",
):
    backend = BackendManager(
        bucket_name=f"{environment}-platform-state",
        region=region,
    )

    backend.ensure_backend()

    executor = EnvironmentDeployer()

    executor.deploy(
        stack,
        environment,
    )
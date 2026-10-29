import logging
import os
import typer

from rit_aws_dri_controller.terraform.deployer import EnvironmentDeployer

terraform_app = typer.Typer()

def get_profile(stack, environment):
    if "AWS_PROFILE" not in os.environ:
        typer.echo(f"""
            AWS_PROFILE environment variable not set.
            
            This allows you to control which AWS profile to use from your AWS CLI configuration.
            
            What I would suggest is either explicitly setting it for the environment, with
            
            export AWS_PROFILE=<profile name>
             
            or ensuring that you have a profile configured called f{stack}-{environment}.
            
            Setting AWS_PROFILE environment variable to f{stack}-{environment} and continuing...
        """)
        os.environ["AWS_PROFILE"] = f"{stack}-{environment}"
    return os.environ["AWS_PROFILE"]

@terraform_app.command()
def deploy(
    stack: str,
    environment: str = "dev",
    region: str = "eu-west-2",
):
    executor = EnvironmentDeployer(stack, environment, region, get_profile(stack, environment))
    executor.plan()

@terraform_app.command()
def plan(
    stack: str,
    environment: str = "dev",
    region: str = "eu-west-2",
):
    executor = EnvironmentDeployer(stack, environment, region, get_profile(stack, environment))
    executor.deploy()
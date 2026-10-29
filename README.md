# rit_aws_dri_controller

## Quick notes on setting up

Run `aws configure sso` to set up the account endpoint you want to use.

Set the region to `eu-west-2` (London) unless you have a different preference, then give things an appropriate profile name and suchlike.

If you don't want to provide the flag, use `AWS_PROFILE`

## Using floci

You can use [floci](https://github.com/floci-io/floci-cli) for local cloud emulation. Follow the install instructions and set up an endpoint to use this instead of the SSO derived credentials above.

When you `floci start`, use the `eval $( floci env )` to set the local environment and that will ensure terraform within the current shell works. As per the docs above, you can visit the [Floci UI](http://localhost:4566/_floci/ui) as well. 

_Note that the floci env output uses `localhost.floci.ui` rather than `localhost`, so add this to your `/etc/hosts` or equivalent.  

# Workflow(s)

## Principle of management

This is very much a work in progress. The theory goes: 

1. Use a new generator to make modules which create new implementations of services (s3_tiered, ebs, ec2 in the above example)
   a. These are setup to be parameterised with typer
   b. The modules track the state of the repository and are committed to this codebase 
2. Stacks get built dynamically with generated / filled in implementations of modules
   a. These are stored within the stacks directory
   b. Stacks could be independently managed repositories tracking against individual accounts, or alternatively one monorepo that can be managed and deployed en masse as changes to the tooling are made.

As modules are updated / new functionality added, previous stacks are either manually updated or recreated to reflect the changes. The latter can be incremental against the existing state, and provenance for the stack outputs (e.g. the commands to recreate the stack) can be stored alongside the terraform.

### Why not just use terraform

Terraform is fantastic against individual accounts, but scaling to manage 100s of accounts is not the easiest, especially when sharing module implementations across accounts. Therefore some controller software offers the ability to update projects en masse and have a singular store of module code that can be used to update (potentially piecemeal) existing environments. 

Each stack ultimately is still an individual terraform project and can be treated as such.

## Terraform structure

The underlying components of the `terraform` directory are given thus. Remember, this is the *controller* for the broader cloud infrastructure!

* `environments`: ...
* `modules`: ...
* `stacks`: ...
* `templates`: ...

## Basic workflow to sanity check configuration

```
# First we generate our modules (using the "general" module is assumed without an additional parameter, which would allow us to define preset templates to copy from using jinja2)
rit-platform module create vpc_dual_w_bastion
rit-platform module create s3_tiered
rit-platform module create github_ecr
rit-platform module create workflow_batch 

# Then we go and edit the structure of the modules to provide an implementation and compose architectural stacks from individual items (batch-implementation-test is just one instance in its own repo! git clone and use this to seed the repo)
rit-platform stack create batch-implementation-test
rit-platform stack add batch-implementation-test test_vpc vpc_dual_w_bastion
rit-platform stack add batch-implementation-test test_store s3_tiered
rit-platform stack add batch-implementation-test test_ecr_ci github_ecr
rit-platform stack add batch-implementation-test test_batch workflow_batch

rit-platform stack list
rit-platform stack show batch-implementation-test
rit-platform terraform plan batch-implementation-test development

# TODO: create more deployed stacks, customising or composing as you need
```

# Things to do!

* [ ] Sort out logging and typer integration (including verbosity setup)

# CREDITS

Written by James Byrne at the University of Exeter 2026.
Some inspiration initially from the UoE copilot instance, which quickly became unhinged.
Gitignore inspiration taken partially (for python) from gitignore.org
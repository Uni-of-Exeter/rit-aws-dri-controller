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

1. Use the module generator to make modules which create implementations of services (s3_tiered, ebs, ec2 in the below example) - `rit-platform module create ...`
   a. You then configure the `module.yaml` to define the module parameters
   b. Implement you module code 
   c. The modules track the state of the repository and are committed to this codebase
2. Stacks get **composed** from modules *and themselves are individual terraform repositories*, using `rit-platform stack create`.
   a. These are stored within the stacks directory. Terraform can be used independently of these tools and ideally these will be stored as separate VCS repositories (do not commit them to this repo!)
   b. Modules are added to stacks with `rit-platform stack add [stack] [module] ...`
   c. Stacks may be initialised against individual accounts for multiple environments. This tool outputs the necessary backend
3. Terraform is then run with `rit-platform terraform ...`
   a. This generates the configuration required for the environment you're running against
   b. The tool can be used to handle the execution, but once in place the stack can be used with `terraform` directly 

As modules are updated and new functionality added, previous stacks can be deployed again to capture the changes made. Stacks can be independently managed as well. 

This all makes `rit-platform` a manner by which to build consistent cloud infrastructure using stacks, update previous ones across multiple environments and accounts easily, and derive new functionality for both modules and new stacks based on controlled tooling rather than error-prone copy-and-paste.

### Why not just use terraform

Terraform is fantastic working with a single repo against a single architecture, but scaling to manage 100s of individual architectures across accounts is not the easiest, especially when sharing module implementations, updates, and consistent code across implementations. Therefore, controller software offers the ability to update projects en masse, generate new implementations quickly, and offer better potential for consisntency which improves security and auditability. 

Each stack ultimately is **still an individual terraform project** and can be treated as such.

## Terraform structure

The underlying components of the `terraform` directory are given thus. Remember, this is the *controller* for the broader cloud infrastructure!

* `modules`: ...
* `stacks`: ...
* `templates`: ...
  * `environments`: ...

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
rit-platform terraform plan batch-implementation-test

# TODO: create more deployed stacks, customising or composing as you need
```

# Things to do!

* [ ] Sort out logging and typer integration (including verbosity setup)
* [ ] Fill out variables when the modules are added to the stack
  * [ ] Do this through initial mapping in code: project level vars to module blocks
  * [ ] Eventually make this a Q&A with the user

# CREDITS

Written by James Byrne at the University of Exeter 2026.
Some inspiration initially from the UoE copilot instance, which quickly became unhinged.
Gitignore inspiration taken partially (for python) from gitignore.org
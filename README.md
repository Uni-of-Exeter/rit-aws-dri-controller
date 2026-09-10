# rit-edris-developments

## Quick notes on setting up

Run `aws configure sso` to set up the account endpoint you want to use.

Set the region to `eu-west-2` (London) unless you have a different preference, then give things an appropriate profile name and suchlike.

If you don't want to provide the flag, use `AWS_PROFILE`

## Using floci

You can use [floci](https://github.com/floci-io/floci-cli) for local cloud emulation. Follow the install instructions and set up an endpoint to use this instead of the SSO derived credentials above.

# Workflow(s)

## Basic workflow to sanity check configuration

```
rit-platform stack create test_datastore
rit-platform stack add test_datastore bucket1 data
rit-platform stack list
rit-platform stack show test_datastore
# TODO: remove terraform from this sequence? It's redundant?
rit-platform terraform deploy 
```

# TODO

This is very much a work in progress. The theory goes: 

1. Use a new generator to take modules and create new implementations, parameterising with typer.
2. Adapt this generation exercise into a jinja based templating workflow that allows more complex stitching together of modules 
3. Stacks are then built from the generated implementations of modules

I would then move the generated terraform configurations into a separate repository with branches for the appropriate environments. This repository then becomes the controller, with the configurations adapting as time goes by. If updates to the modules are required, they could be merged and / or recreated in the target repository.

# CREDITS

Written by James Byrne at the University of Exeter 2026.
Some inspiration initially from the UoE copilot instance, which quickly became unhinged.
Gitignore inspiration taken partially (for python) from gitignore.org
import os
from pathlib import Path

import yaml

class StackRenderer:
    def __init__(self, stacks_dir: os.PathLike ='terraform/stacks'):
        self.stacks_dir = Path(stacks_dir)

    def render(self, stack_name: str):
        stack_dir = self.stacks_dir / stack_name
        stack = yaml.safe_load((stack_dir / 'stack.yaml').read_text())

        out = "".join([f"""module "{m["name"]}" {{
  source = "../../modules/implementations/{m["type"]}"
}}
""" for m in stack['modules']])
        (stack_dir / 'main.tf').write_text(out)

        # TODO: add variables required
        # TODO: update git if present
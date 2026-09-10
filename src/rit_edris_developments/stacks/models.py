from dataclasses import dataclass

@dataclass
class StackModule:
    name: str
    type: str


@dataclass
class Stack:
    name: str
    modules: list[StackModule]
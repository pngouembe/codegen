from dataclasses import dataclass, field
from typing import List

from internal.classes import InternalClass
from internal.functions import InternalFunction
from internal.variable import InternalVariable


@dataclass
class InternalNamespace:
    name: List[str]
    functions: List[InternalFunction] = field(default_factory=list)
    variables: List[InternalVariable] = field(default_factory=list)
    classes: List[InternalClass] = field(default_factory=list)

    def __post_init__(self):
        self.internal_name = ".".join(self.name)

    def update(self, other):
        self.functions += (other.functions)
        self.variables += (other.variables)
        self.classes += (other.classes)

    def add_class(self, cls: InternalClass):
        self.classes.append(cls)

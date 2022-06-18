from dataclasses import dataclass, field
from typing import List

from internal.classes import InternalClass
from internal.enums import InternalEnum
from internal.functions import InternalFunction
from internal.variable import InternalVariable


@dataclass
class InternalNamespace:
    name: List[str]
    functions: List[InternalFunction] = field(default_factory=list)
    variables: List[InternalVariable] = field(default_factory=list)
    classes: List[InternalClass] = field(default_factory=list)
    enums: List[InternalEnum] = field(default_factory=list)

    def __post_init__(self):
        self.internal_name = ""
        self._update_internal_name()

    def _update_internal_name(self):
        self.internal_name = ".".join(self.name)

    def update(self, other):
        self.functions += (other.functions)
        self.variables += (other.variables)
        self.classes += (other.classes)
        self.enums += (other.enums)

    def add_class(self, cls: InternalClass):
        self.classes.append(cls)

    def add_function(self, cls: InternalFunction):
        self.functions.append(cls)

    def add_variable(self, cls: InternalVariable):
        self.variables.append(cls)

    def add_enum(self, cls: InternalEnum):
        self.enums.append(cls)

    def add_namespace(self, namespace):
        self.name.extend(namespace.name)
        self._update_internal_name
        self.update(namespace)

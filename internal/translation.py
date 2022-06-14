from dataclasses import dataclass, field
from os.path import join
from typing import Dict, List

from internal.classes import InternalClass
from internal.enums import InternalEnum
from internal.functions import InternalFunction
from internal.namespace import InternalNamespace


@dataclass
class UnitTranslation:
    name: str
    classes: List[InternalClass] = field(default_factory=list)
    functions: List[InternalFunction] = field(default_factory=list)
    namespaces: Dict[str, InternalNamespace] = field(default_factory=dict)
    enums: List[InternalEnum] = field(default_factory=list)

    def add_namespace(self, namespace: InternalNamespace):
        if namespace.internal_name in self.namespaces.keys():
            self.namespaces[namespace.internal_name].update(namespace)
        else:
            self.namespaces[namespace.internal_name] = namespace

    def add_class(self, cls: InternalClass):
        self.classes.append(cls)

    def add_enum(self, cls: InternalEnum):
        self.enums.append(cls)

    def add_function(self, function: InternalFunction):
        self.functions.append(function)


@dataclass
class GeneratedOutput:
    name: str
    content: str
    path: str = "."

    def get_path(self) -> str:
        return join(self.path, self.name)

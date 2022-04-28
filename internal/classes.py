from dataclasses import dataclass, field
from typing import List

from internal.attributes import InternalAttribute
from internal.functions import InternalFunction
from internal.visibility import Visibility


@dataclass
class InternalClass:
    name: str
    functions: List[InternalFunction] = field(default_factory=list)
    attributes: List[InternalAttribute] = field(default_factory=list)
    parent_classes: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.public_functions = [
            f for f in self.functions if f.visibility == Visibility.PUBLIC]
        self.private_functions = [
            f for f in self.functions if f.visibility == Visibility.PRIVATE]
        self.protected_functions = [
            f for f in self.functions if f.visibility == Visibility.PROTECTED]

    def add_function(self, function: InternalFunction):
        self.functions.append(function)

    def add_attribute(self, attribute: InternalAttribute):
        self.attributes.append(attribute)

    def add_attribute(self, parent_classes: str):
        self.parent_classes.append(parent_classes)
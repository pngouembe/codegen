from dataclasses import dataclass, field
from typing import List

from internal.attributes import InternalAttribute


@dataclass
class InternalEnum:
    name: str
    attributes: List[InternalAttribute] = field(default_factory=list)
    parent_classes: List[str] = field(default_factory=list)

    def add_attribute(self, attribute: InternalAttribute):
        self.attributes.append(attribute)

    def add_parent_class(self, parent_classes: str):
        self.parent_classes.append(parent_classes)

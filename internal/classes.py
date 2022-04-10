from dataclasses import dataclass, field
from typing import List

from internal.attributes import InternalAttribute
from internal.functions import InternalFunction


@dataclass
class InternalClass:
    name: str
    functions: List[InternalFunction] = field(default_factory=list)
    attributes: List[InternalAttribute] = field(default_factory=list)
    namespaces: List[str] = None
    parent_classes: List[str] = field(default_factory=list)

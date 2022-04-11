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
    namespaces: List[str] = None
    parent_classes: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.public_functions = [
            f for f in self.functions if f.visibility == Visibility.PUBLIC]
        self.private_functions = [
            f for f in self.functions if f.visibility == Visibility.PRIVATE]
        self.protected_functions = [
            f for f in self.functions if f.visibility == Visibility.PROTECTED]

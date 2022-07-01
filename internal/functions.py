from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Set

from internal.arguments import InternalArgument
from internal.types import InternalType
from internal.visibility import Visibility


class FunctionModifiers(Enum):
    CONST = auto()
    VIRTUAL = auto()
    ABSTRACT = auto()


@dataclass
class InternalFunction:
    name: str
    arguments: List[InternalArgument] = field(default_factory=list)
    return_type: InternalType = None
    visibility: Visibility = Visibility.PUBLIC
    modifiers: Set[FunctionModifiers] = field(default_factory=set)
    doc: List[str] = field(default_factory=list)
    extra_elem: str = None

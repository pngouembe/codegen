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

    #TODO: Put this CPP representation in CPP function class
    def __repr__(self) -> str:
        rep_str = ""
        if FunctionModifiers.VIRTUAL in self.modifiers or FunctionModifiers.ABSTRACT in self.modifiers:
            rep_str += "virtual "
        if self.return_type:
            rep_str += f"{self.return_type!r} "
        args_str = ", ".join([repr(a) for a in self.arguments])

        rep_str += f"{self.name}({args_str})"

        if FunctionModifiers.CONST in self.modifiers:
            rep_str += " const"

        if FunctionModifiers.ABSTRACT in self.modifiers:
            rep_str += " = 0"

        rep_str += ";"

        return rep_str

from dataclasses import dataclass, field
from typing import List

from internal.arguments import InternalArgument
from internal.types import InternalType
from internal.visibility import Visibility


@dataclass
class InternalFunction:
    name: str
    arguments: List[InternalArgument] = field(default_factory=list)
    return_type: InternalType = None
    visibility: Visibility = Visibility.PUBLIC

    def __repr__(self) -> str:
        rep_str = ""
        if self.return_type:
            rep_str = f"{self.return_type!r} "
        args_str = ", ".join([repr(a) for a in self.arguments])

        rep_str = f"{rep_str}{self.name}({args_str})"

        return rep_str

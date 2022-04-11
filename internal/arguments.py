from dataclasses import dataclass

from internal.types import InternalType


@dataclass
class InternalArgument:
    name: str
    type: InternalType = None
    default_value: str = None

    def __repr__(self) -> str:
        rep_str = f"{self.name}"
        if self.type:
            rep_str = f"{self.type!r} {rep_str}"

        if self.default_value:
            rep_str = f"{rep_str} = {self.default_value}"

        return rep_str

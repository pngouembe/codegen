from dataclasses import dataclass

from internal.types import InternalType


@dataclass
class InternalArgument:
    name: str
    type: InternalType = None

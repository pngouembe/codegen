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

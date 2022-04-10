from dataclasses import dataclass

from internal.types import InternalType
from internal.visibility import Visibility


@dataclass
class InternalAttribute:
    name: str
    visibility: Visibility = Visibility.PUBLIC
    type: InternalType = None

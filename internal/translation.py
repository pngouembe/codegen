from dataclasses import dataclass, field
from typing import List

from internal.classes import InternalClass
from internal.functions import InternalFunction


@dataclass
class UnitTranslation:
    name: str
    classes: List[InternalClass] = field(default_factory=list)
    functions: List[InternalFunction] = field(default_factory=list)

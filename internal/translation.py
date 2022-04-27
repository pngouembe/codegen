from dataclasses import dataclass, field
from os.path import join
from typing import List

from internal.classes import InternalClass
from internal.functions import InternalFunction


@dataclass
class UnitTranslation:
    name: str
    classes: List[InternalClass] = field(default_factory=list)
    functions: List[InternalFunction] = field(default_factory=list)

@dataclass
class GeneratedOutput:
    name: str
    content: str
    path: str = "."

    def get_path(self) -> str:
        return join(self.path, self.name)
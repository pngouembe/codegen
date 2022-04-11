from dataclasses import dataclass
from typing import List


@dataclass
class InternalType:
    name: str

    def __repr__(self) -> str:
        return f"{self.name}"

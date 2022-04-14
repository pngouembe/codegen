from dataclasses import dataclass
from typing import List


@dataclass
class InternalType:
    name: str
    namespace: List[str] = None
    namespace_sep: str = "."

    def __repr__(self) -> str:
        if self.namespace:
            return self.namespace_sep.join(self.namespace + [self.name])
        return f"{self.name}"

from dataclasses import dataclass
from intermediate.types import CodegenType


@dataclass
class CTypes(CodegenType):
    @classmethod
    def from_str(cls, string: str):
        return cls(name=string.strip())

    def to_str(self) -> str:
        return self.name

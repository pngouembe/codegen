from dataclasses import dataclass
from intermediate.types import CodegenType


@dataclass
class CTypes(CodegenType):
    @classmethod
    def from_str(cls, string: str):
        return cls(name=string.strip())

    @classmethod
    def from_inter_lang(cls, elem: CodegenType):
        return cls(elem.name)

    def to_str(self) -> str:
        return self.name

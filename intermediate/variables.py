from dataclasses import dataclass
from intermediate.types import CodegenType


@dataclass
class CodegenVariable:
    name: str
    type: CodegenType

    def to_inter_lang(self):
        return CodegenVariable(self.name, self.type.to_inter_lang())

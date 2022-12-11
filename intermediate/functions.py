from dataclasses import dataclass
from intermediate.types import CodegenType
from intermediate.variables import CodegenVariable
from typing import List


@dataclass
class CodegenFunction:
    return_type: CodegenType
    name: str
    args: List[CodegenVariable]


    def to_inter_lang(self):
        return CodegenFunction(
            self.return_type.to_inter_lang(),
            self.name,
            [arg.to_inter_lang() for arg in self.args]
        )

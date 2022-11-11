from dataclasses import dataclass
from intermediate.types import CodegenType
from intermediate.variables import CodegenVariable
from typing import List


@dataclass
class CodegenFunction:
    return_type: CodegenType
    name: str
    args: List[CodegenVariable]

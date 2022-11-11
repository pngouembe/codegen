from dataclasses import dataclass
from intermediate.types import CodegenType


@dataclass
class CodegenVariable:
    name: str
    type: CodegenType

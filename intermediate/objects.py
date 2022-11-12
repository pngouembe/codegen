from dataclasses import dataclass
from intermediate.variables import CodegenVariable
from intermediate.functions import CodegenFunction
from typing import List


@dataclass
class CodegenObject:
    name: str
    public_attributes: List[CodegenVariable]
    protected_attributes: List[CodegenVariable]
    private_attributes: List[CodegenVariable]
    public_functions: List[CodegenFunction]
    protected_functions: List[CodegenFunction]
    private_functions: List[CodegenFunction]

    def to_inter_lang(self):
        return CodegenObject(
            self.name,
            [attr.to_inter_lang() for attr in self.public_attributes],
            [attr.to_inter_lang() for attr in self.protected_attributes],
            [attr.to_inter_lang() for attr in self.private_attributes],
            [func.to_inter_lang() for func in self.public_functions],
            [func.to_inter_lang() for func in self.protected_functions],
            [func.to_inter_lang() for func in self.private_functions]
        )

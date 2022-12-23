from dataclasses import dataclass
from intermediate.translationunit import CodegenTranslationUnit
from .c_variables import CVariable
from .c_functions import CFunction
from .c_objects import CObject


@dataclass
class CTranslationUnit(CodegenTranslationUnit):
    @classmethod
    def from_inter_lang(cls, elem: CodegenTranslationUnit):
        return cls(
            [CVariable.from_inter_lang(var) for var in elem.variables],
            [CFunction.from_inter_lang(func) for func in elem.funtions],
            [CObject.from_inter_lang(obj) for obj in elem.objects]
        )

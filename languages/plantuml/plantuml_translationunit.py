from dataclasses import dataclass
from intermediate.translationunit import CodegenTranslationUnit
from .plantuml_variables import PlantumlVariable
from .plantuml_functions import PlantumlFunction
from .plantuml_objects import PlantumlObject


@dataclass
class PlantumlTranslationUnit(CodegenTranslationUnit):
    @classmethod
    def from_inter_lang(cls, elem: CodegenTranslationUnit):
        return cls(
            [PlantumlVariable.from_inter_lang(var) for var in elem.variables],
            [PlantumlFunction.from_inter_lang(func) for func in elem.funtions],
            [PlantumlObject.from_inter_lang(obj) for obj in elem.objects]
        )

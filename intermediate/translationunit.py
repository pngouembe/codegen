from dataclasses import dataclass, field
from typing import List
from .variables import CodegenVariable
from .functions import CodegenFunction
from .objects import CodegenObject


@dataclass
class CodegenTranslationUnit:
    variables: List[CodegenVariable] = field(default_factory=list)
    funtions: List[CodegenFunction] = field(default_factory=list)
    objects: List[CodegenObject] = field(default_factory=list)

    def to_inter_lang(self):
        return CodegenTranslationUnit(
            variables=[var.to_inter_lang() for var in self.variables],
            funtions=[func.to_inter_lang() for func in self.funtions],
            objects=[obj.to_inter_lang() for obj in self.objects]
        )

    def add(self, element):
        if issubclass(type(element), CodegenVariable):
            self.variables.append(element.to_inter_lang())
        elif issubclass(type(element), CodegenFunction):
            self.funtions.append(element.to_inter_lang())
        elif issubclass(type(element), CodegenObject):
            self.objects.append(element.to_inter_lang())
        else:
            raise ValueError

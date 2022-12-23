from dataclasses import dataclass, field
from typing import List
from intermediate.variables import CodegenVariable
from intermediate.functions import CodegenFunction
from intermediate.objects import CodegenObject


@dataclass
class TranslationUnit:
    variables: List[CodegenVariable] = field(default_factory=list)
    funtions: List[CodegenFunction] = field(default_factory=list)
    objects: List[CodegenObject] = field(default_factory=list)

    def add(self, element):
        if isinstance(element, CodegenVariable):
            self.variables.append(element)
        elif isinstance(element, CodegenFunction):
            self.funtions.append(element)
        elif isinstance(element, CodegenObject):
            self.objects.append(element)
        else:
            raise ValueError

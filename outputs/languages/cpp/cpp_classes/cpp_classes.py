from dataclasses import dataclass

from internal.classes import InternalClass
from outputs.interfaces import LanguageSpecificClass

from ..cpp_attributes import CppAttribute
from ..cpp_functions import CppFunction


@dataclass(repr=False)
class CppClass(LanguageSpecificClass):

    @classmethod
    def from_internal(cls, internal: InternalClass):
        f_list = [CppFunction.from_internal(f) for f in internal.functions]
        a_list = [CppAttribute.from_internal(a) for a in internal.attributes]
        return cls(name=internal.name,
                   functions=f_list,
                   attributes=a_list,
                   parent_classes=internal.parent_classes)

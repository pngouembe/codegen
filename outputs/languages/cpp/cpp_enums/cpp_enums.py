from dataclasses import dataclass

from internal.enums import InternalEnum
from outputs.interfaces import LanguageSpecificEnum

from ..cpp_attributes import CppAttribute


@dataclass(repr=False)
class CppEnum(LanguageSpecificEnum):

    @classmethod
    def from_internal(cls, internal: InternalEnum):
        a_list = [CppAttribute.from_internal(a) for a in internal.attributes]
        return cls(name=internal.name,
                   attributes=a_list,
                   parent_classes=internal.parent_classes)

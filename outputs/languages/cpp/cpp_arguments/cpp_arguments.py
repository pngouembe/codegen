from dataclasses import dataclass

from internal.arguments import InternalArgument
from outputs.interfaces import LanguageSpecificArgument

from ..cpp_types import CppTypes


@dataclass(repr=False)
class CppArgument(LanguageSpecificArgument):
    @classmethod
    def from_internal(cls, internal: InternalArgument):
        a_type = CppTypes.from_internal(
            internal.type) if internal.type else None
        return cls(name=internal.name,
                   type=a_type,
                   default_value=internal.default_value)

from dataclasses import dataclass

from internal.variable import InternalVariable
from outputs.interfaces import LanguageSpecificVariable

from ..cpp_types import CppTypes


@dataclass(repr=False)
class CppVariable(LanguageSpecificVariable):
    @classmethod
    def from_internal(cls, internal: InternalVariable):
        a_type = CppTypes.from_internal(
            internal.type) if internal.type else None
        return cls(name=internal.name,
                   type=a_type,
                   default_value=internal.default_value)

    def __repr__(self) -> str:
        repr_str = "" if self.type is None else repr(self.type) + " "
        repr_str = repr_str + self.name
        if self.default_value:
            repr_str = repr_str + " = " + self.default_value

        return repr_str

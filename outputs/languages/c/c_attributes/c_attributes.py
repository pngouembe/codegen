from dataclasses import dataclass

from internal.attributes import InternalAttribute
from outputs.interfaces import LanguageSpecificAttribute

from ..c_types import CTypes


@dataclass(repr=False)
class CAttribute(LanguageSpecificAttribute):
    @classmethod
    def from_internal(cls, internal: InternalAttribute):
        a_type = CTypes.from_internal(
            internal.type) if internal.type else None
        return cls(name=internal.name,
                   type=a_type,
                   default_value=internal.default_value,
                   visibility=internal.visibility)

    def __repr__(self) -> str:
        repr_str = "" if self.type is None else repr(self.type) + " "
        repr_str = repr_str + self.name
        if self.default_value:
            repr_str = repr_str + " = " + self.default_value

        return repr_str

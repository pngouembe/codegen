from dataclasses import dataclass
import re

from internal.functions import FunctionModifiers, InternalFunction
from outputs.interfaces import LanguageSpecificFunction

from ..gmock_arguments import GmockArgument
from ..gmock_types import GmockTypes

CPP_FUNCTION_MODIFIERS = {
    "const": FunctionModifiers.CONST
}

@dataclass(repr=False)
class GmockFunction(LanguageSpecificFunction):

    @classmethod
    def from_internal(cls, internal: InternalFunction):
        a_list = [GmockArgument.from_internal(a) for a in internal.arguments]
        return_type = GmockTypes.from_internal(
            internal.return_type) if internal.return_type else None

        if internal.extra_elem:
            for mod in CPP_FUNCTION_MODIFIERS.keys():
                if mod in internal.extra_elem:
                    internal.modifiers.add(CPP_FUNCTION_MODIFIERS[mod])
                    internal.extra_elem = re.sub(mod, "", internal.extra_elem)
        return cls(name=internal.name,
                   arguments=a_list,
                   return_type=return_type,
                   visibility=internal.visibility,
                   modifiers=internal.modifiers,
                   extra_elem=internal.extra_elem)

    def __repr__(self) -> str:
        rep_str = "MOCK_METHOD("
        if self.return_type:
            rep_str += f"{self.return_type!r}, "
        else:
            rep_str += "void, "
        rep_str += f"{self.name}, "
        args_str = ", ".join([repr(a.type) for a in self.arguments if a.type is not None])
        rep_str += f"({args_str}), "
        modifier_list = list()
        if FunctionModifiers.VIRTUAL in self.modifiers or FunctionModifiers.ABSTRACT in self.modifiers:
            modifier_list.append("override")
        if FunctionModifiers.CONST in self.modifiers:
            modifier_list.append("const")
        modifier_str = ', '.join(modifier_list)
        rep_str += f"({modifier_str})"
        rep_str += ")"
        return rep_str

from dataclasses import dataclass

from internal.functions import FunctionModifiers, InternalFunction
from outputs.interfaces import LanguageSpecificFunction

from ..cpp_arguments import CppArgument
from ..cpp_types import CppTypes


@dataclass(repr=False)
class CppFunction(LanguageSpecificFunction):

    @classmethod
    def from_internal(cls, internal: InternalFunction):
        a_list = [CppArgument.from_internal(a) for a in internal.arguments]
        return_type = CppTypes.from_internal(
            internal.return_type) if internal.return_type else None

        return cls(name=internal.name,
                   arguments=a_list,
                   return_type=return_type,
                   visibility=internal.visibility,
                   modifiers=internal.modifiers)

    def __repr__(self) -> str:
        rep_str = ""
        if FunctionModifiers.VIRTUAL in self.modifiers or FunctionModifiers.ABSTRACT in self.modifiers:
            rep_str += "virtual "
        if self.return_type:
            rep_str += f"{self.return_type!r} "
        args_str = ", ".join([repr(a) for a in self.arguments])

        rep_str += f"{self.name}({args_str})"

        if FunctionModifiers.CONST in self.modifiers:
            rep_str += " const"

        if FunctionModifiers.ABSTRACT in self.modifiers:
            rep_str += " = 0"

        rep_str += ";"

        return rep_str

from dataclasses import dataclass
import re

from internal.functions import FunctionModifiers, InternalFunction
from outputs.interfaces import LanguageSpecificFunction

from ..cpp_arguments import CppArgument
from ..cpp_types import CppTypes

CPP_FUNCTION_MODIFIERS = {
    "const": FunctionModifiers.CONST
}

@dataclass(repr=False)
class CppFunction(LanguageSpecificFunction):

    @classmethod
    def from_internal(cls, internal: InternalFunction):
        a_list = [CppArgument.from_internal(a) for a in internal.arguments]
        return_type = CppTypes.from_internal(
            internal.return_type) if internal.return_type else None
        # TODO: Find a better way to keep the indentation
        if internal.doc:
            doc_list = ["/**"]
            doc_list.extend([f"     * {l}" for l in internal.doc])
            doc_list.append("     */\n    ")
        else:
            doc_list = list()
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
                   doc=doc_list,
                   extra_elem=internal.extra_elem)

    def __repr__(self) -> str:
        if self.doc:
            rep_str = "\n".join(self.doc)
        else:
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

        if self.extra_elem:
            rep_str += f" {self.extra_elem}"

        return rep_str

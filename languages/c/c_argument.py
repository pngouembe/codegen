from dataclasses import dataclass
from languages.c.c_types import CTypes
from intermediate.variables import CodegenVariable


@dataclass
class CArgument(CodegenVariable):

    @classmethod
    def from_str(cls, string: str):
        string = string.replace(";", "")
        type_str, name = string.rsplit(maxsplit=1)
        return cls(
            name=name.strip(),
            type=CTypes.from_str(type_str.strip()),
        )

    @classmethod
    def from_inter_lang(cls, elem: CodegenVariable):
        return cls(elem.name, CTypes.from_inter_lang(elem.type))

    def to_str(self) -> str:
        return f"{self.type.to_str()} {self.name}"

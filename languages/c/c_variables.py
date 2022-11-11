from dataclasses import dataclass
from languages.c.c_types import CTypes
from intermediate.variables import CodegenVariable


@dataclass
class CVariable(CodegenVariable):
    semi_colon_terminated: bool = False

    @classmethod
    def from_str(cls, string: str):
        semi_colon = False
        if string.strip().endswith(";"):
            semi_colon = True
            string = string.replace(";", "")
        type_str, name = string.rsplit(maxsplit=1)
        return cls(
            name=name.strip(),
            type=CTypes.from_str(type_str.strip()),
            semi_colon_terminated=semi_colon
        )

    def to_str(self) -> str:
        end_of_line = ";" if self.semi_colon_terminated else ""
        return f"{self.type.to_str()} {self.name}{end_of_line}"

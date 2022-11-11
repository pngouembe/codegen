from dataclasses import dataclass
from languages.c.c_types import CTypes
from languages.c.c_variables import CVariable
from intermediate.functions import CodegenFunction


@dataclass
class CFunction(CodegenFunction):
    @classmethod
    def from_str(cls, string: str):
        return_type, tmp = string.split(maxsplit=1)
        return_type = CTypes.from_str(return_type)
        name, args_str = tmp.split("(", maxsplit=1)
        args_str = args_str.replace(")", "").replace(";", "")
        args = [CVariable.from_str(arg) for arg in args_str.split(",")]
        return cls(
            return_type=return_type,
            name=name,
            args=args
        )

    def to_str(self) -> str:
        args_str = ",".join([arg.to_str() for arg in self.args])
        return f"{self.return_type.to_str()} {self.name}({args_str});"

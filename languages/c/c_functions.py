from dataclasses import dataclass
from languages.c.c_types import CTypes
from languages.c.c_argument import CArgument
from intermediate.functions import CodegenFunction


@dataclass
class CFunction(CodegenFunction):
    @classmethod
    def from_str(cls, string: str):
        return_type, tmp = string.split(maxsplit=1)
        return_type = CTypes.from_str(return_type)
        name, args_str = tmp.split("(", maxsplit=1)
        args_str = args_str.replace(")", "").replace(";", "")
        args = [CArgument.from_str(arg) for arg in args_str.split(",")]
        return cls(
            return_type=return_type,
            name=name,
            args=args
        )

    @classmethod
    def from_inter_lang(cls, elem: CodegenFunction):
        return cls(
            CTypes.from_inter_lang(elem.return_type),
            elem.name,
            [CArgument.from_inter_lang(arg) for arg in elem.args]
        )

    def to_str(self) -> str:
        args_str = ", ".join([arg.to_str() for arg in self.args])
        return f"{self.return_type.to_str()} {self.name}({args_str});"


@dataclass
class CFunctionPointer(CFunction):
    @classmethod
    def from_function(cls, function: CFunction):
        cls(
            function.return_type,
            function.name,
            function.args
        )

    def to_str(self) -> str:
        args_str = ", ".join([arg.type.to_str() for arg in self.args])
        return f"{self.return_type.to_str()} (*{self.name})({args_str});"

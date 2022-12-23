from dataclasses import dataclass
from languages.plantuml.plantuml_types import PlantumlType
from languages.plantuml.plantuml_variables import PlantumlVariable
from intermediate.functions import CodegenFunction


@dataclass
class PlantumlFunction(CodegenFunction):
    @classmethod
    def from_str(cls, string: str):

        name = ""
        args_str = ""
        type_str = ""

        # TODO: Error cases
        name, string = string.split("(", maxsplit=1)
        args_str, type_str = string.rsplit(")", maxsplit=1)

        type_str = type_str.lstrip(": ").strip()

        args = [PlantumlVariable.from_str(arg.strip())
                for arg in args_str.split(",")]

        return cls(
            return_type=PlantumlType.from_str(type_str),
            name=name,
            args=args
        )

    @classmethod
    def from_inter_lang(cls, elem: CodegenFunction):
        return cls(
            PlantumlType.from_inter_lang(elem.return_type),
            elem.name,
            [PlantumlVariable.from_inter_lang(arg) for arg in elem.args]
        )

    def to_str(self) -> str:
        args_str = ", ".join([arg.to_str() for arg in self.args])
        return f"{self.name}({args_str}) : {self.return_type.to_str()}"

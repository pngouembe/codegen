from intermediate.variables import CodegenVariable
from languages.plantuml.plantuml_types import PlantumlType


class PlantumlVariable(CodegenVariable):
    @classmethod
    def from_str(cls, string: str):
        name = ""
        type_str = ""
        if ':' in string:
            name, type_str = string.split(':')
        else:
            name = string

        name = name.strip()
        type_str = type_str.strip()

        return cls(
            name=name,
            type=PlantumlType.from_str(type_str)
        )

    @classmethod
    def from_inter_lang(cls, elem: CodegenVariable):
        return cls(elem.name, PlantumlType.from_inter_lang(elem.type))

    def to_str(self) -> str:
        if self.name:
            return f"{self.name} : {self.type.to_str()}"
        else:
            return ""

from intermediate.types import CodegenType


class PlantumlType(CodegenType):
    @classmethod
    def from_str(cls, string: str):
        name = string

        return cls(
            name=name
        )

    @classmethod
    def from_inter_lang(cls, elem: CodegenType):
        return cls(elem.name)

    def to_str(self) -> str:
        return self.name

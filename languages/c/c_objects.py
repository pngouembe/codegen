from dataclasses import dataclass
from jinja2 import Environment, PackageLoader, select_autoescape
from languages.c.c_variables import CVariable
from languages.c.c_functions import CFunctionPointer
from intermediate.objects import CodegenObject


@dataclass
class CObject(CodegenObject):

    def __post_init__(self) -> None:
        self.env = Environment(
            loader=PackageLoader(__package__),
            autoescape=select_autoescape)

    @classmethod
    def from_str(cls, string: str):
        string = string.removeprefix("struct").strip()
        name, tmp = string.split("{", maxsplit=1)
        name = name.strip()

        body, _ = tmp.rsplit("}", maxsplit=1)
        functions = []
        for func in body.split(";"):
            if func:
                functions.append(CFunctionPointer.from_str(func))
        return cls(
            name=name,
            public_attributes=[],
            protected_attributes=[],
            private_attributes=[],
            public_functions=functions,
            protected_functions=[],
            private_functions=[]
        )

    @classmethod
    def from_inter_lang(cls, elem: CodegenObject):
        return cls(
            elem.name,
            [CVariable.from_inter_lang(attr)
             for attr in elem.public_attributes],
            [CVariable.from_inter_lang(attr)
             for attr in elem.protected_attributes],
            [CVariable.from_inter_lang(attr)
             for attr in elem.private_attributes],
            [CFunctionPointer.from_inter_lang(attr)
             for attr in elem.public_functions],
            [CFunctionPointer.from_inter_lang(attr)
             for attr in elem.protected_functions],
            [CFunctionPointer.from_inter_lang(attr)
             for attr in elem.private_functions]
        )

    def to_str(self) -> str:
        j2_template = self.env.get_template("c_object.j2")
        return j2_template.render(**self.__dict__)

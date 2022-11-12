from dataclasses import dataclass
from languages.c.c_variables import CVariable
from languages.c.c_functions import CFunction
from intermediate.objects import CodegenObject


@dataclass
class CObject(CodegenObject):
    @classmethod
    def from_str(cls, string: str):
        string = string.removeprefix("struct").strip()
        name, tmp = string.split("{", maxsplit=1)
        name = name.strip()

        body, _ = tmp.rsplit("}", maxsplit=1)
        functions = []
        for func in body.split(";"):
            if func:
                functions.append(CFunction.from_str(func))
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
            [CFunction.from_inter_lang(attr)
             for attr in elem.public_functions],
            [CFunction.from_inter_lang(attr)
             for attr in elem.protected_functions],
            [CFunction.from_inter_lang(attr)
             for attr in elem.private_functions]
        )

    def to_str(self) -> str:
        function_str = str("\n".join([func.to_str()
                                      for func in self.public_functions]))

        print(function_str)
        ret_str = "struct %s { %s };" % (self.name, function_str)
        return ret_str

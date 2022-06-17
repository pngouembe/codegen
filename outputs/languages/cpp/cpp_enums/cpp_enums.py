from dataclasses import dataclass

from internal.enums import InternalEnum
from jinja2 import Environment, PackageLoader
from outputs.interfaces import LanguageSpecificEnum

from ..cpp_attributes import CppAttribute

CPP_ENUM_TEMPLATE = "cpp_enum.j2"

@dataclass(repr=False)
class CppEnum(LanguageSpecificEnum):

    @classmethod
    def from_internal(cls, internal: InternalEnum):
        a_list = [CppAttribute.from_internal(a) for a in internal.attributes]
        return cls(name=internal.name,
                   attributes=a_list,
                   parent_classes=internal.parent_classes)

    def __repr__(self) -> str:
        env = Environment(loader=PackageLoader(__name__))
        template = env.get_template(CPP_ENUM_TEMPLATE)
        return template.render(enum=self)

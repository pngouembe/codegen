from dataclasses import dataclass
from os import path

from internal.classes import InternalClass
from jinja2 import Environment, FileSystemLoader
from outputs.interfaces import LanguageSpecificClass

from ..c_attributes import CAttribute
from ..c_functions import CFunction

c_CLASS_TEMPLATE_PATH = path.join(path.dirname(__file__), "templates/")
c_CLASS_TEMPLATE = "c_class.j2"


@dataclass(repr=False)
class CClass(LanguageSpecificClass):
    @classmethod
    def from_internal(cls, internal: InternalClass):
        f_list = [CFunction.from_internal(f) for f in internal.functions]
        a_list = [CAttribute.from_internal(a) for a in internal.attributes]
        return cls(name=internal.name,
                   functions=f_list,
                   attributes=a_list,
                   parent_classes=internal.parent_classes)

    def __repr__(self) -> str:

        env = Environment(loader=FileSystemLoader(c_CLASS_TEMPLATE_PATH))
        template = env.get_template(c_CLASS_TEMPLATE)
        return template.render(cls=self)

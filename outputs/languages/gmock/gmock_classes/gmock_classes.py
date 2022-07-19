from dataclasses import dataclass
from os import path

from internal.classes import InternalClass
from jinja2 import Environment, FileSystemLoader
from outputs.interfaces import LanguageSpecificClass

from ..gmock_functions import GmockFunction

# TODO: Use the cpp class template
GMOCK_CLASS_TEMPLATE_PATH = path.join(path.dirname(__file__), "templates/")
GMOCK_CLASS_TEMPLATE = "gmock_class.j2"

@dataclass(repr=False)
class GmockClass(LanguageSpecificClass):
    @classmethod
    def from_internal(cls, internal: InternalClass):
        f_list = [GmockFunction.from_internal(f) for f in internal.functions]

        # Removing the destructor from the function list
        destructor_indexes = []
        for i, f in enumerate(f_list):
            if f.name.startswith("~"):
                destructor_indexes.append(i)
        for i in destructor_indexes:
            f_list.pop(i)

        c_name = internal.name + "Mock"
        return cls(name=c_name,
                   functions=f_list,
                   parent_classes=[internal.name])

    def __repr__(self) -> str:

        env = Environment(loader=FileSystemLoader(GMOCK_CLASS_TEMPLATE_PATH))
        template = env.get_template(GMOCK_CLASS_TEMPLATE)
        return template.render(cls=self)
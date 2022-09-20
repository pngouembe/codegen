from dataclasses import dataclass

from internal.namespace import InternalNamespace
from jinja2 import Environment, FileSystemLoader
from mylogger import log
from os import path
from outputs.interfaces import LanguageSpecificNamespace

from ..c_classes import CClass
from ..c_enums import CEnum
from ..c_functions import CFunction
from ..c_variables import CVariable

c_NAMESPACE_TEMPLATE_PATH = path.join(path.dirname(__file__), "templates/")
c_NAMESPACE_TEMPLATE = "c_namespace.j2"


@dataclass(repr=False)
class CNamespaces(LanguageSpecificNamespace):

    @classmethod
    def from_internal(cls, internal: InternalNamespace):
        log.debug(f"Converting {internal.internal_name} namespace")
        log.debug(internal)
        f_list = [CFunction.from_internal(f) for f in internal.functions]
        v_list = [CVariable.from_internal(v) for v in internal.variables]
        c_list = [CClass.from_internal(c) for c in internal.classes]
        e_list = [CEnum.from_internal(e) for e in internal.enums]
        return cls(name=internal.name,
                   functions=f_list,
                   variables=v_list,
                   classes=c_list,
                   enums=e_list)

    def __repr__(self) -> str:
        env = Environment(loader=FileSystemLoader(c_NAMESPACE_TEMPLATE_PATH))
        template = env.get_template(c_NAMESPACE_TEMPLATE)
        return template.render(ns=self)

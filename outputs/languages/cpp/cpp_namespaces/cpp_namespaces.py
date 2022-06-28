from dataclasses import dataclass

from internal.namespace import InternalNamespace
from jinja2 import Environment, FileSystemLoader
from mylogger import log
from os import path
from outputs.interfaces import LanguageSpecificNamespace

from ..cpp_classes import CppClass
from ..cpp_enums import CppEnum
from ..cpp_functions import CppFunction
from ..cpp_variables import CppVariable

CPP_NAMESPACE_TEMPLATE_PATH = path.join(path.dirname(__file__), "templates/")
CPP_NAMESPACE_TEMPLATE = "cpp_namespace.j2"

@dataclass(repr=False)
class CppNamespaces(LanguageSpecificNamespace):

    @classmethod
    def from_internal(cls, internal: InternalNamespace):
        log.debug(f"Converting {internal.internal_name} namespace")
        log.debug(internal)
        f_list = [CppFunction.from_internal(f) for f in internal.functions]
        v_list = [CppVariable.from_internal(v) for v in internal.variables]
        c_list = [CppClass.from_internal(c) for c in internal.classes]
        e_list = [CppEnum.from_internal(e) for e in internal.enums]
        return cls(name=internal.name,
                   functions=f_list,
                   variables=v_list,
                   classes=c_list,
                   enums=e_list)

    def __repr__(self) -> str:
        env = Environment(loader=FileSystemLoader(CPP_NAMESPACE_TEMPLATE_PATH))
        template = env.get_template(CPP_NAMESPACE_TEMPLATE)
        return template.render(ns=self)

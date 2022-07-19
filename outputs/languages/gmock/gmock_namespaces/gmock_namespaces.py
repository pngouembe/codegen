from dataclasses import dataclass

from internal.namespace import InternalNamespace
from jinja2 import Environment, FileSystemLoader
from mylogger import log
from os import path
from outputs.interfaces import LanguageSpecificNamespace

from ..gmock_classes import GmockClass

GMOCK_NAMESPACE_TEMPLATE_PATH = path.join(path.dirname(__file__), "templates/")
GMOCK_NAMESPACE_TEMPLATE = "gmock_namespace.j2"

@dataclass(repr=False)
class GmockNamespaces(LanguageSpecificNamespace):

    @classmethod
    def from_internal(cls, internal: InternalNamespace):
        log.debug(f"Converting {internal.internal_name} namespace")
        log.debug(internal)
        c_list = [GmockClass.from_internal(c) for c in internal.classes]
        return cls(name=internal.name, classes=c_list)

    def __repr__(self) -> str:
        env = Environment(loader=FileSystemLoader(GMOCK_NAMESPACE_TEMPLATE_PATH))
        template = env.get_template(GMOCK_NAMESPACE_TEMPLATE)
        return template.render(ns=self)

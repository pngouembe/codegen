from os import path

from internal.translation import GeneratedOutput, UnitTranslation
from jinja2 import Environment, FileSystemLoader
from mylogger import log
from outputs.interfaces import LanguageSpecificGenerator

from outputs.languages.gmock.gmock_classes import GmockClass
from outputs.languages.gmock.gmock_namespaces import GmockNamespaces

from config import config


GMOCK_TEMPLATE_PATH = path.join(path.dirname(__file__), "templates/")
GMOCK_TEMPLATE = "gmock_template.j2"

class GmockGenerator(LanguageSpecificGenerator):
    def translate(self, unit_translation: UnitTranslation, config: config.CodegenConfig) -> GeneratedOutput:
        env = Environment(loader=FileSystemLoader(GMOCK_TEMPLATE_PATH))

        template = env.get_template(GMOCK_TEMPLATE)

        log.debug("Translating to GMOCK:")
        log.debug(f"Template: {GMOCK_TEMPLATE}")
        log.debug(f"Unit: {unit_translation}")

        self.cls_list = [GmockClass.from_internal(c)
                         for c in unit_translation.classes]
        self.ns_list = [GmockNamespaces.from_internal(ns)
                         for ns in unit_translation.namespaces.values()]


        # TODO: Create include guard from the file path or global namespace
        include_guard = str.upper(unit_translation.name + "mock_hpp")

        include = unit_translation.name + ".hpp"

        log.debug(f"include : {include}")
        ret_str = template.render(header=config.header, CODEGEN_LOCK=config.codegen_lock, ns_list=self.ns_list, cls_list=self.cls_list,
                                  include_guard=include_guard, include=include)
        file_name = unit_translation.name + "mock.hpp"
        return GeneratedOutput(name=file_name, content=ret_str)
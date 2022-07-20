"""CPP class objects"""

from os import path

import yaml
from config.config import CodegenConfig
from internal.translation import GeneratedOutput, UnitTranslation
from jinja2 import Environment, FileSystemLoader
from mylogger import log
from outputs.interfaces import LanguageSpecificGenerator
from outputs.languages.cpp.cpp_config.cpp_constants import (INCLUDE_CFG_FILE,
                                                            STD_INCLUDE_FILE,
                                                            TEMPLATE_NAME)
from outputs.languages.cpp.cpp_config.cpp_includes import (
    INCLUDE_FILES_DICT, INCLUDE_FILES_SET, INCLUDE_WARNINGS_SET,
    update_include_file_matcher_dict)

from outputs.languages.cpp.cpp_classes import CppClass
from outputs.languages.cpp.cpp_enums import CppEnum
from outputs.languages.cpp.cpp_functions import CppFunction
from outputs.languages.cpp.cpp_namespaces import CppNamespaces

CPP_TEMPLATE_PATH = path.join(path.dirname(__file__), "templates/")
CPP_TEMPLATE = "cpp_template.j2"

class CppGenerator(LanguageSpecificGenerator):
    def translate(self, unit_translation: UnitTranslation, config: CodegenConfig) -> GeneratedOutput:
        env = Environment(loader=FileSystemLoader(CPP_TEMPLATE_PATH))

        if config.language_custom_config.CPP.custom_include_file_dict:
            INCLUDE_FILES_DICT.update(config.language_custom_config.CPP.custom_include_file_dict)
        else:
            log.warn(
                f'No custom includes file provided, using the types found in "{STD_INCLUDE_FILE}"')

        update_include_file_matcher_dict()

        template = env.get_template(TEMPLATE_NAME)

        log.debug("Translating to CPP:")
        log.debug(f"Template: {TEMPLATE_NAME}")
        log.debug(f"Unit: {unit_translation}")

        self.cls_list = [CppClass.from_internal(c)
                         for c in unit_translation.classes]
        self.enum_list = [CppEnum.from_internal(e)
                          for e in unit_translation.enums]
        self.fct_list = [CppFunction.from_internal(f)
                         for f in unit_translation.functions]
        self.ns_list = [CppNamespaces.from_internal(ns)
                        for ns in unit_translation.namespaces.values()]

        # TODO: Create include guard from the file path or global namespace
        include_guard = str.upper(unit_translation.name + "_hpp")

        includes_set = sorted(INCLUDE_FILES_SET.copy())
        INCLUDE_FILES_SET.clear()
        for w in INCLUDE_WARNINGS_SET:
            log.warn(w)
        INCLUDE_WARNINGS_SET.clear()

        log.debug(f"include set : {includes_set}")
        ret_str = template.render(header=config.header, CODEGEN_LOCK=config.codegen_lock, ns_list=self.ns_list, cls_list=self.cls_list,
                                  include_guard=include_guard, includes_set=includes_set, enum_list=self.enum_list)
        file_name = unit_translation.name + ".hpp"
        return GeneratedOutput(name=file_name, content=ret_str)

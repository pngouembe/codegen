"""CPP class objects"""

from os import path

import yaml
from internal.translation import GeneratedOutput, UnitTranslation
from jinja2 import Environment, PackageLoader
from mylogger import log
from outputs.interfaces import LanguageSpecificGenerator
from outputs.languages.cpp.cpp_config.cpp_constants import (INCLUDE_CFG_FILE,
                                                            STD_INCLUDE_FILE,
                                                            TEMPLATE_NAME)
from outputs.languages.cpp.cpp_config.cpp_includes import (
    INCLUDE_FILES_DICT, INCLUDE_FILES_SET, update_include_file_matcher_dict)

from .cpp_classes import CppClass
from .cpp_enums import CppEnum
from .cpp_functions import CppFunction
from .cpp_namespaces import CppNamespaces


class CppGenerator(LanguageSpecificGenerator):
    def translate(self, unit_translation: UnitTranslation) -> GeneratedOutput:
        env = Environment(loader=PackageLoader("outputs"))

        try:
            with open(path.join(INCLUDE_CFG_FILE)) as f:
                INCLUDE_FILES_DICT.update(yaml.safe_load(f))
        except FileNotFoundError:
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
        includes_set
        INCLUDE_FILES_SET.clear()
        log.debug(f"include set : {includes_set}")
        ret_str = template.render(ns_list=self.ns_list, cls_list=self.cls_list, include_guard=include_guard,
                                  includes_set=includes_set)
        file_name = unit_translation.name + ".hpp"
        return GeneratedOutput(name=file_name, content=ret_str)

"""CPP class objects"""

from enum import Enum
from typing import List
from xml.etree.ElementInclude import include
import yaml

from mylogger import log
from dataclasses import dataclass, field
from os import path

from internal.arguments import InternalArgument
from internal.attributes import InternalAttribute
from internal.classes import InternalClass
from internal.functions import InternalFunction
from internal.namespace import InternalNamespace
from internal.translation import GeneratedOutput, UnitTranslation
from internal.types import InternalType
from jinja2 import Environment, PackageLoader
from internal.variable import InternalVariable
from outputs.interfaces import (LanguageSpecificArgument,
                                LanguageSpecificAttribute,
                                LanguageSpecificClass,
                                LanguageSpecificFunction,
                                LanguageSpecificGenerator, LanguageSpecificNamespace,
                                LanguageSpecificType, LanguageSpecificVariable)

CPP_NAMESPACE_SEP = "::"
INCLUDE_FILES_SET = set()
INCLUDE_FILES_DICT = dict()

# Initializing the types to include file dictionnary
with open(path.join(path.dirname(__file__),"./cpp_types.yml")) as f:
    INCLUDE_FILES_DICT = yaml.load(f)

INCLUDE_FILE_MATCHER_DICT = {}
def update_include_file_matcher_dict():
    for key, values in INCLUDE_FILES_DICT.items():
        for val in values:
            INCLUDE_FILE_MATCHER_DICT[val] = key

class CppTypeModifier(Enum):
    CONST = "const "
    CONST_POINTER = "* const "
    POINTER = "*"
    CONST_REFERENCE = "& const "
    REFERENCE = "&"


@dataclass(repr=False)
class CppTypes(LanguageSpecificType):
    @classmethod
    def from_internal(cls, internal: InternalType):
        internal.namespace_sep = CPP_NAMESPACE_SEP
        tmp_str = repr(internal)
        tmp_str = tmp_str.replace("&", " &").replace("*", " *")
        for m in [mod.value for mod in CppTypeModifier]:
            if m in tmp_str:
                tmp_str = tmp_str.replace(m, "")
        str_list: List[str] = list()
        for elem in tmp_str.split("<"):
            str_list.append(elem.replace(">", ""))

        for s in str_list:
            s = s.strip()
            log.debug(f"Found type: {s}")
            try:
                include_file = INCLUDE_FILE_MATCHER_DICT[s]
                if include_file != "builtin":
                    INCLUDE_FILES_SET.add(INCLUDE_FILE_MATCHER_DICT[s])
            except KeyError:
                if CPP_NAMESPACE_SEP in s:
                    s = s.rsplit(CPP_NAMESPACE_SEP, maxsplit=1)[-1]
                    try:
                        include_file = INCLUDE_FILE_MATCHER_DICT[s]
                        if include_file != "builtin":
                            INCLUDE_FILES_SET.add(INCLUDE_FILE_MATCHER_DICT[s])
                    except KeyError:
                        log.warn(f"Warning {s} is an unknown type")
                else:
                    log.warn(f"Warning {s} is an unknown type")
        return cls(name=internal.name, namespace=internal.namespace, namespace_sep=CPP_NAMESPACE_SEP)


@dataclass(repr=False)
class CppArgument(LanguageSpecificArgument):
    @classmethod
    def from_internal(cls, internal: InternalArgument):
        a_type = CppTypes.from_internal(
            internal.type) if internal.type else None
        return cls(name=internal.name,
                   type=a_type,
                   default_value=internal.default_value)


@dataclass(repr=False)
class CppAttribute(LanguageSpecificAttribute):
    @classmethod
    def from_internal(cls, internal: InternalAttribute):
        a_type = CppTypes.from_internal(
            internal.type) if internal.type else None
        return cls(name=internal.name,
                   type=a_type,
                   default_value=internal.default_value,
                   visibility=internal.visibility)


@dataclass(repr=False)
class CppVariable(LanguageSpecificVariable):
    @classmethod
    def from_internal(cls, internal: InternalVariable):
        a_type = CppTypes.from_internal(
            internal.type) if internal.type else None
        return cls(name=internal.name,
                   type=a_type,
                   default_value=internal.default_value)


@dataclass(repr=False)
class CppFunction(LanguageSpecificFunction):

    @classmethod
    def from_internal(cls, internal: InternalFunction):
        a_list = [CppArgument.from_internal(a) for a in internal.arguments]
        return_type = CppTypes.from_internal(
            internal.return_type) if internal.return_type else None

        return cls(name=internal.name,
                   arguments=a_list,
                   return_type=return_type,
                   visibility=internal.visibility,
                   modifiers=internal.modifiers)


@dataclass(repr=False)
class CppClass(LanguageSpecificClass):

    @classmethod
    def from_internal(cls, internal: InternalClass):
        f_list = [CppFunction.from_internal(f) for f in internal.functions]
        a_list = [CppAttribute.from_internal(a) for a in internal.attributes]
        return cls(name=internal.name,
                   functions=f_list,
                   attributes=a_list,
                   parent_classes=internal.parent_classes)


@dataclass(repr=False)
class CppNamespaces(LanguageSpecificNamespace):

    @classmethod
    def from_internal(cls, internal: InternalNamespace):
        log.debug(f"Converting {internal.internal_name} namespace")
        log.debug(internal)
        f_list = [CppFunction.from_internal(f) for f in internal.functions]
        v_list = [CppVariable.from_internal(v) for v in internal.variables]
        c_list = [CppClass.from_internal(c) for c in internal.classes]
        return cls(name=internal.name,
                   functions=f_list,
                   variables=v_list,
                   classes=c_list)



class CppGenerator(LanguageSpecificGenerator):
    def translate(self, unit_translation: UnitTranslation) -> GeneratedOutput:
        env = Environment(loader=PackageLoader("outputs"))
        template_name = 'cpp_template.j2'
        include_cfg_file = 'cpp_custom_includes.yml'
        with open(path.join(include_cfg_file)) as f:
            INCLUDE_FILES_DICT.update(yaml.load(f))
        update_include_file_matcher_dict()

        template = env.get_template(template_name)

        log.debug("Translating to CPP:")
        log.debug(f"Template: {template_name}")
        log.debug(f"Unit: {unit_translation}")

        self.cls_list = [CppClass.from_internal(c)
                         for c in unit_translation.classes]
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

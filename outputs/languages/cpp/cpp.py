"""CPP class objects"""

import yaml

from dataclasses import dataclass
from os import path

from internal.arguments import InternalArgument
from internal.attributes import InternalAttribute
from internal.classes import InternalClass
from internal.functions import InternalFunction
from internal.translation import UnitTranslation
from internal.types import InternalType
from jinja2 import Environment, PackageLoader
from outputs.interfaces import (LanguageSpecificArgument,
                                LanguageSpecificAttribute,
                                LanguageSpecificClass,
                                LanguageSpecificFunction,
                                LanguageSpecificGenerator,
                                LanguageSpecificType)

CPP_NAMESPACE_SEP = "::"
INCLUDE_FILES_SET = set()

# Initializing the types to include file dictionnary
with open(path.join(path.dirname(__file__),"./cpp_types.yml")) as f:
    INCLUDE_FILES_DICT = yaml.load(f)

REVERSED_INCLUDE_FILES_DICT = {}
for key, values in INCLUDE_FILES_DICT.items():
    for val in values:
        REVERSED_INCLUDE_FILES_DICT[val] = key

@dataclass(repr=False)
class CppTypes(LanguageSpecificType):
    @classmethod
    def from_internal(cls, internal: InternalType):
        try:
            INCLUDE_FILES_SET.add(REVERSED_INCLUDE_FILES_DICT[repr(internal)])
        except KeyError:
            print(f"Warning {internal!r} is an unknown type")
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
                   namespaces=internal.namespaces,
                   parent_classes=internal.parent_classes)


class CppGenerator(LanguageSpecificGenerator):
    def translate(self, unit_translation: UnitTranslation) -> str:
        env = Environment(loader=PackageLoader("outputs"))
        template = env.get_template('cpp_template.j2')

        self.cls_list = [CppClass.from_internal(c)
                         for c in unit_translation.classes]
        self.fct_list = [CppFunction.from_internal(f)
                         for f in unit_translation.functions]

        # TODO: Create include guard from the file path or global namespace
        include_guard = str.upper(unit_translation.name + "_hpp")

        includes_set = INCLUDE_FILES_SET.copy()
        INCLUDE_FILES_SET.clear()

        sep1 = "-"*80+"\n"
        sep2 = "\n"+"*"*80+"\n"

        print(sep1)
        print(template.render(cls_list=self.cls_list, include_guard=include_guard,
                includes_set=includes_set), end=sep2)

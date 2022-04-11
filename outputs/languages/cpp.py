"""CPP class objects"""

from dataclasses import dataclass
from enum import Enum

from internal.arguments import InternalArgument
from internal.attributes import InternalAttribute
from internal.classes import InternalClass
from internal.functions import InternalFunction
from internal.translation import UnitTranslation
from internal.types import InternalType
from internal.visibility import Visibility
from jinja2 import Environment, PackageLoader
from outputs.interfaces import (LanguageSpecificArgument,
                                LanguageSpecificAttribute,
                                LanguageSpecificClass,
                                LanguageSpecificFunction,
                                LanguageSpecificGenerator,
                                LanguageSpecificType)

CPP_NAMESPACE_SEP = "::"


class CppTypeEnum(Enum):
    VOID = 'void'
    INT = 'int'
    CHAR = 'char'

# TODO: Check known types


@dataclass(repr=False)
class CppTypes(LanguageSpecificType):
    @classmethod
    def from_internal(cls, internal: InternalType):

        return cls(name=internal.name)


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
                   visibility=internal.visibility)


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
    def translate(self, unit_translation: UnitTranslation) -> None:
        env = Environment(loader=PackageLoader("outputs"))
        template = env.get_template('cpp_template.j2')

        self.cls_list = [CppClass.from_internal(c)
                         for c in unit_translation.classes]
        self.fct_list = [CppFunction.from_internal(f)
                         for f in unit_translation.functions]

        # TODO: Create include guard from the file path or global namespace
        include_guard = "dummy_include_guard"

        # TODO: Create the include list based on the type encoutered during unit translation
        includes_list = ['<iostream>', '"my_test_header.hpp"']

        sep1 = "-"*80+"\n"
        sep2 = "\n"+"*"*80+"\n"

        for cls in self.cls_list:
            print(sep1)
            print(template.render(cls=cls, include_guard=include_guard,
                  includes_list=includes_list), end=sep2)

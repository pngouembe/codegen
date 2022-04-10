"""CPP class objects"""

from dataclasses import dataclass, field
from typing import List

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


class CppTypes(LanguageSpecificType):
    VOID = 'void'
    INT = 'int'
    CHAR = 'char'

    @classmethod
    def from_internal(cls, internal: InternalType):
        return cls(internal)


@dataclass
class CppArgument(LanguageSpecificArgument):
    name: str
    type: LanguageSpecificType = CppTypes.VOID

    @classmethod
    def from_internal(cls, internal: InternalArgument):
        return cls(internal.name)

    def __repr__(self) -> str:
        if self.name:
            return f"{self.type.value} {self.name}"
        else:
            return ""


@dataclass
class CppAttribute(LanguageSpecificAttribute):
    name: str
    visibility: Visibility = Visibility.PUBLIC
    type: LanguageSpecificType = CppTypes.VOID

    @classmethod
    def from_internal(cls, internal: InternalAttribute):
        return cls(internal.name)


@dataclass
class CppFunction(LanguageSpecificFunction):
    name: str
    arguments: List[LanguageSpecificArgument] = field(default_factory=list)
    return_type: LanguageSpecificType = CppTypes.VOID
    visibility: Visibility = Visibility.PUBLIC

    @classmethod
    def from_internal(cls, internal: InternalFunction):
        a_list = [CppArgument.from_internal(a) for a in internal.arguments]
        try:
            return_type = CppTypes(internal.return_type)
        except:
            return_type = CppTypes.VOID

        return cls(name=internal.name,
                   arguments=a_list,
                   return_type=return_type,
                   visibility=internal.visibility)

    def __repr__(self) -> str:
        args = [repr(a) for a in self.arguments]
        return "{} {}({})".format(self.return_type.value, self.name, ",".join(args))


@dataclass
class CppClass(LanguageSpecificClass):
    name: str
    functions: List[LanguageSpecificFunction] = field(default_factory=list)
    attributes: List[LanguageSpecificAttribute] = field(default_factory=list)
    namespaces: List[str] = None
    parent_classes: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.public_functions = [
            f for f in self.functions if f.visibility == Visibility.PUBLIC]
        self.private_functions = [
            f for f in self.functions if f.visibility == Visibility.PRIVATE]
        self.protected_functions = [
            f for f in self.functions if f.visibility == Visibility.PROTECTED]

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

        for cls in self.cls_list:
            print(template.render(cls=cls))

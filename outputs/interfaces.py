from dataclasses import dataclass

from internal.arguments import InternalArgument
from internal.attributes import InternalAttribute
from internal.classes import InternalClass
from internal.enums import InternalEnum
from internal.functions import InternalFunction
from internal.namespace import InternalNamespace
from internal.translation import GeneratedOutput, UnitTranslation
from internal.types import InternalType
from internal.variable import InternalVariable


class LanguageSpecificGenerator:
    def translate(self, unit_translation: UnitTranslation) -> GeneratedOutput:
        pass


@dataclass(repr=False)
class LanguageSpecificNamespace(InternalNamespace):
    @classmethod
    def from_internal(cls, internal: InternalNamespace):
        pass


@dataclass(repr=False)
class LanguageSpecificEnum(InternalEnum):
    @classmethod
    def from_internal(cls, internal: InternalEnum):
        pass


@dataclass(repr=False)
class LanguageSpecificClass(InternalClass):
    @classmethod
    def from_internal(cls, internal: InternalClass):
        pass


@dataclass(repr=False)
class LanguageSpecificFunction(InternalFunction):
    @classmethod
    def from_internal(cls, internal: InternalFunction):
        pass


@dataclass(repr=False)
class LanguageSpecificAttribute(InternalAttribute):
    @classmethod
    def from_internal(cls, internal: InternalAttribute):
        pass


@dataclass(repr=False)
class LanguageSpecificArgument(InternalArgument):
    @classmethod
    def from_internal(cls, internal: InternalArgument):
        pass


@dataclass(repr=False)
class LanguageSpecificVariable(InternalVariable):
    @classmethod
    def from_internal(cls, internal: InternalVariable):
        pass


class LanguageSpecificType(InternalType):
    @classmethod
    def from_internal(cls, internal: InternalType):
        pass

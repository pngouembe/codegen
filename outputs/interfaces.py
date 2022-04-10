from dataclasses import dataclass
from enum import Enum

from internal.arguments import InternalArgument
from internal.attributes import InternalAttribute
from internal.classes import InternalClass
from internal.functions import InternalFunction
from internal.translation import UnitTranslation
from internal.types import InternalType


class LanguageSpecificGenerator:
    def translate(self, unit_translation: UnitTranslation) -> None:
        pass


@dataclass
class LanguageSpecificClass:
    @classmethod
    def from_internal(cls, internal: InternalClass):
        pass


@dataclass
class LanguageSpecificFunction:
    @classmethod
    def from_internal(cls, internal: InternalFunction):
        pass


@dataclass
class LanguageSpecificAttribute:
    @classmethod
    def from_internal(cls, internal: InternalAttribute):
        pass


@dataclass
class LanguageSpecificArgument:
    @classmethod
    def from_internal(cls, internal: InternalArgument):
        pass


class LanguageSpecificType(Enum):
    @classmethod
    def from_internal(cls, internal: InternalType):
        pass

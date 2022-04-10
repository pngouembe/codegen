from enum import Enum, auto

from outputs.languages import cpp


class OutputLanguages(Enum):
    CPP = cpp.CppGenerator

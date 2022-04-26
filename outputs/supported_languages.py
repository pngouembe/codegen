from enum import Enum

from outputs.languages import cpp


class OutputLanguages(Enum):
    CPP = cpp.CppGenerator

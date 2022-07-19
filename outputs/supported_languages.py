from enum import Enum

from outputs.languages import cpp, gmock


class OutputLanguages(Enum):
    CPP = cpp.CppGenerator
    GMOCK = gmock.GmockGenerator

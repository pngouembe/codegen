from enum import Enum

from outputs.languages import c, cpp, gmock


class OutputLanguages(Enum):
    CPP = cpp.CppGenerator
    GMOCK = gmock.GmockGenerator
    C = c.CGenerator

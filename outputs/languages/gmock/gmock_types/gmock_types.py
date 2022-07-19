from dataclasses import dataclass
from outputs.languages.cpp import cpp_types

@dataclass(repr=False)
class GmockTypes(cpp_types.CppTypes):
    ...
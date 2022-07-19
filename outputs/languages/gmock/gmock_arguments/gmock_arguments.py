from dataclasses import dataclass
from outputs.languages.cpp import cpp_arguments

@dataclass(repr=False)
class GmockArgument(cpp_arguments.CppArgument):
    ...
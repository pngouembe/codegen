from enum import Enum, auto

from inputs.languages import xmi


class InputLanguages(Enum):
    CPP_XMI = xmi.CppXmiParser

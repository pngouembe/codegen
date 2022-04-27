from enum import Enum

from inputs.languages import xmi


class InputLanguages(Enum):
    CPP_XMI = xmi.CppXmiParser

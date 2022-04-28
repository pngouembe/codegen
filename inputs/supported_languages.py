from enum import Enum

from inputs.languages import xmi, plantuml


class InputLanguages(Enum):
    CPP_XMI = xmi.CppXmiParser
    PLANTUML = plantuml.PlantumlParser

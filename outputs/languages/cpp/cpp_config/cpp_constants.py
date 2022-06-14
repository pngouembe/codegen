from enum import Enum

CPP_NAMESPACE_SEP = "::"
TEMPLATE_NAME = 'cpp_template.j2'
STD_INCLUDE_FILE = './cpp_types.yml'
INCLUDE_CFG_FILE = 'cpp_custom_includes.yml'


class CppTypeModifier(Enum):
    CONST = "const "
    CONST_POINTER = "* const "
    POINTER = "*"
    CONST_REFERENCE = "& const "
    REFERENCE = "&"

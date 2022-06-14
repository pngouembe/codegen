from dataclasses import dataclass
from typing import List

from internal.types import InternalType
from mylogger import log
from outputs.interfaces import LanguageSpecificType
from outputs.languages.cpp.cpp_config.cpp_constants import (CPP_NAMESPACE_SEP,
                                                            CppTypeModifier)
from outputs.languages.cpp.cpp_config.cpp_includes import (
    INCLUDE_FILE_MATCHER_DICT, INCLUDE_FILES_SET)


@dataclass(repr=False)
class CppTypes(LanguageSpecificType):
    @classmethod
    def from_internal(cls, internal: InternalType):
        internal.namespace_sep = CPP_NAMESPACE_SEP
        tmp_str = repr(internal)
        tmp_str = tmp_str.replace("&", " &").replace("*", " *")
        for m in [mod.value for mod in CppTypeModifier]:
            if m in tmp_str:
                tmp_str = tmp_str.replace(m, "")
        str_list: List[str] = list()
        for elem in tmp_str.split("<"):
            str_list.append(elem.replace(">", ""))

        for s in str_list:
            s = s.strip()
            log.debug(f"Found type: {s}")
            try:
                include_file = INCLUDE_FILE_MATCHER_DICT[s]
                if include_file != "builtin":
                    INCLUDE_FILES_SET.add(INCLUDE_FILE_MATCHER_DICT[s])
            except KeyError:
                if CPP_NAMESPACE_SEP in s:
                    s = s.rsplit(CPP_NAMESPACE_SEP, maxsplit=1)[-1]
                    try:
                        include_file = INCLUDE_FILE_MATCHER_DICT[s]
                        if include_file != "builtin":
                            INCLUDE_FILES_SET.add(INCLUDE_FILE_MATCHER_DICT[s])
                    except KeyError:
                        log.warn(f"Warning {s} is an unknown type")
                else:
                    log.warn(f"Warning {s} is an unknown type")
        return cls(name=internal.name, namespace=internal.namespace, namespace_sep=CPP_NAMESPACE_SEP)

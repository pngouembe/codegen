from dataclasses import dataclass
from typing import List

from internal.utility import list_namespaces


@dataclass
class InternalType:
    name: str
    namespace: List[str] = None
    namespace_sep: str = "."

    @classmethod
    def from_string(cls, string: str, namespace_sep: str = None):
        if namespace_sep == None:
            namespace_sep = cls.namespace_sep
        try:
            ns, name = string.rsplit(namespace_sep, maxsplit=1)
        except ValueError:
            ns = None
            name = string
        else:
            ns = list_namespaces(string=ns, namespace_sep=namespace_sep)

        return cls(name=name, namespace=ns, namespace_sep=namespace_sep)

import re


def list_namespaces(string: str, namespace_sep: str = None):
    if namespace_sep:
        return string.split(f"{namespace_sep}")
    else:
        return re.split(r"[\.\:]+", string)

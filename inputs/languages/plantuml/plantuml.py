import re
from dataclasses import dataclass
from os import path

import yaml
from inputs.interfaces import LanguageSpecificParser
from internal.arguments import InternalArgument
from internal.classes import InternalClass
from internal.functions import FunctionModifiers, InternalFunction
from internal.namespace import InternalNamespace
from internal.translation import UnitTranslation
from internal.types import InternalType
from internal.visibility import Visibility
from mylogger import log

with open(path.join(path.dirname(__file__), "./keywords.yml")) as f:
    PLANTUML_KEYWORDS = yaml.load(f)

PLANTUML_VISIBILITY_MATCHER = {
    "+": Visibility.PUBLIC,
    "-": Visibility.PRIVATE,
    "#": Visibility.PROTECTED,
    "~": Visibility.PACKAGE_PRIVATE
}

PLANTUML_FUNCTION_MODIFIER_MATCHER = {
    "{abstract}": FunctionModifiers.ABSTRACT,
    "{method}": None,
}


def function_from_str(str: str) -> InternalFunction:
    str = str.strip()
    try:
        pre_args, tmp = str.split("(", maxsplit=1)
    except ValueError:
        pre_args = str
        args = post_args = None
    else:
        try:
            args, post_args = tmp.rsplit(")", maxsplit=1)
        except ValueError:
            args = tmp

    try:
        pre_name, f_name = pre_args.rsplit(maxsplit=1)
    except ValueError:
        f_name = pre_args
        pre_name = ""

    f_type = None
    modifiers = set()
    try:
        visibility = PLANTUML_VISIBILITY_MATCHER[pre_name[0]]
    except KeyError:
        visibility = Visibility.PUBLIC
    else:
        pre_name = pre_name[1::]

    for elem in pre_name.split():
        try:
            modifiers.add(PLANTUML_FUNCTION_MODIFIER_MATCHER[elem])
        except KeyError:
            pass
        else:
            continue

        # At this point the elem can be considered as a return type
        f_type = InternalType.from_string(elem)

    arg_list = list()
    if args:
        for arg in args.split(","):
            arg = arg.strip()
            arg_list.append(InternalArgument.from_string(arg))

    return InternalFunction(name=f_name, arguments=arg_list, return_type=f_type, visibility=visibility, modifiers=modifiers)


PLANTUML_KEYWORD_MATCHER = {
    "namespace": InternalNamespace,
    "interface": InternalClass,
}


@dataclass
class PlantumlParser(LanguageSpecificParser):
    def translate(self, file: str) -> UnitTranslation:
        with open(file, "r") as f:
            file_content = f.read().splitlines()

        unit = UnitTranslation(name=path.splitext(path.basename(file))[0])

        ns_sep = "."
        context = [unit]
        for line in file_content:
            if line.strip().startswith("'"):
                # this is a commented line, ignore it
                continue

            if line.strip().startswith("@"):
                # this is a line to ignore
                continue

            if line.strip().upper().startswith("NOTE"):
                # this is a line to ignore
                continue

            # Retrieving the name after namespace and before the {
            m = re.search(r"namespace\s+([^\{\s]+)", line, re.IGNORECASE)
            if m:
                log.debug(f"Found a namespace: {m.group(1)}")
                ns = InternalNamespace(name=m.group(1).split(ns_sep))
                context.append(ns)
                line = line.split(m.group(0), maxsplit=1)[-1]

            # Retrieving the name after interface and before the {
            m = re.search(r"interface\s+([^\{\s]+)", line, re.IGNORECASE)
            if m:
                log.debug(f"Found a interface: {m.group(1)}")
                cls = InternalClass(name=m.group(1))
                if "{" in line:
                    context.append(cls)
                line = line.split(m.group(0), maxsplit=1)[-1]

            # Retrieving the name after class and before the {
            m = re.search(r"class\s+([^\{\s]+)", line, re.IGNORECASE)
            if m:
                log.debug(f"Found a class: {m.group(1)}")
                cls = InternalClass(name=m.group(1))
                if "{" in line:
                    context.append(cls)
                line = line.split(m.group(0), maxsplit=1)[-1]

            # Check if method identifiers are in the line
            m = re.search(r"(\{method\}|\{abstract\}).*", line)
            if m:
                function = function_from_str(line)
                log.debug(f"function repr: {function}")
                try:
                    context[-1].add_function(function)
                except IndexError:
                    log.warn(f"Index problem with the current context: {context}")
                line = line.split(m.group(0), maxsplit=1)[-1]

            # Check if the line contains something similar to a function signature with parenthesis
            m = re.search(r"[^\(]+\([^\)]*\).*", line)
            if m:
                function = function_from_str(line)
                log.debug(f"function repr: {function}")
                try:
                    context[-1].add_function(function)
                except IndexError:
                    log.warn(f"Index problem with the current context: {context}")

                line = line.split(m.group(0), maxsplit=1)[-1]

            m = re.search(r"\}", line)
            if m:
                try:
                    if isinstance(context[-1], InternalClass):
                        context[-2].add_class(context[-1])
                    elif isinstance(context[-1], InternalNamespace):
                        context[-2].add_namespace(context[-1])
                    context.pop()
                    line = line.split(m.group(0), maxsplit=1)[-1]
                except IndexError:
                    log.warn(f"Index problem with the current context: {context}")

        return unit

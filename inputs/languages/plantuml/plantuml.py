import yaml
from internal.arguments import InternalArgument
from internal.classes import InternalClass
from internal.functions import InternalFunction

from mylogger import log

from dataclasses import dataclass
from os import path

import re

from inputs.interfaces import LanguageSpecificParser
from internal.namespace import InternalNamespace
from internal.translation import UnitTranslation

with open(path.join(path.dirname(__file__),"./keywords.yml")) as f:
    PLANTUML_KEYWORDS = yaml.load(f)


def function_from_str(str:str) -> InternalFunction:
    log.debug(f"Found a function: {m.group(0)}")
    log.debug(f"visibility: {m.group(1)}")
    log.debug(f"option: {m.group(2)}")
    log.debug(f"signature: {m.group(3)}")
    # log.debug(f"args: {m.group(4)}")
    f_type = None
    try:
        f_type, f_name = m.group(3).split()
    except ValueError:
        f_name = m.group(3)
    function = InternalFunction(name=f_name, return_type=f_type)

PLANTUML_KEYWORD_MATCHER = {
    "namespace": InternalNamespace,
    "interface": InternalClass,
}


@dataclass
class PlantumlParser(LanguageSpecificParser):
    def translate(self, file: str) -> UnitTranslation:
        with open(file, "r") as f:
            file_content = f.readlines()

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
                context.append(cls)
                line = line.split(m.group(0), maxsplit=1)[-1]

            # r"([\+\-\#\~])?\s+(\{abstract\}|\{method\}|\{static\})?\s+([^\(]+)(\([^\)]*\))?"
            m = re.search(r"(\{method\}|\{abstract\})(.)(.*)", line)
            if m:

                log.debug(function)
                context[-1].add_function(function)
                line = line.split(m.group(0), maxsplit=1)[-1]


            m = re.search(r"([^\(]*\()(.)(.*)", line)
            if m:
                log.debug(f"Found a function: {m.group(0)}")
                log.debug(f"visibility: {m.group(1)}")
                log.debug(f"option: {m.group(2)}")
                log.debug(f"signature: {m.group(3)}")
                # log.debug(f"args: {m.group(4)}")
                f_type = None
                try:
                    f_type, f_name = m.group(3).split()
                except ValueError:
                    f_name = m.group(3)
                function = InternalFunction(name=f_name, return_type=f_type)
                log.debug(function)
                context[-1].add_function(function)
                line = line.split(m.group(0), maxsplit=1)[-1]


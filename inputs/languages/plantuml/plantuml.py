import re
from dataclasses import dataclass
from os import path
from typing import Dict, Tuple

from inputs.interfaces import LanguageSpecificParser
from internal.arguments import InternalArgument
from internal.attributes import InternalAttribute
from internal.classes import InternalClass
from internal.enums import InternalEnum
from internal.functions import FunctionModifiers, InternalFunction
from internal.namespace import InternalNamespace
from internal.translation import UnitTranslation
from internal.types import InternalType
from internal.visibility import Visibility
from mylogger import log

PLANTUML_VISIBILITY_MATCHER = {
    "+": Visibility.PUBLIC,
    "-": Visibility.PRIVATE,
    "#": Visibility.PROTECTED,
    "~": Visibility.PACKAGE_PRIVATE
}

PLANTUML_ARROWS = {
    "<|--",
    "--|>",
    "o--*",
    "*--*",
    "*--o",
}

# TODO: support the const modifier
PLANTUML_FUNCTION_MODIFIER_MATCHER = {
    "{abstract}": FunctionModifiers.ABSTRACT,
    "{method}": None,
}

PLANTUML_CONTEXT_KEYWORDS = {
    "namespace": InternalNamespace,
    "class": InternalClass,
    "enum": InternalEnum,
    "interface": InternalClass,
    "abstract class": InternalClass,
}


def attribute_from_str(str: str) -> InternalAttribute:
    tmp = str.split()
    try:
        a_visibility = PLANTUML_VISIBILITY_MATCHER[tmp[0]]
        tmp.pop(0)
    except KeyError:
        # No visibility given, using Public as default
        a_visibility = Visibility.PUBLIC

    if tmp[0] == "{field}":
        tmp.pop(0)

    if len(tmp) >= 3 and tmp[-2] == "=":
        a_default = tmp[-1]
        tmp = tmp[:-2]
    else:
        a_default = None

    if len(tmp) >= 3 and tmp[1] == ":":
        a_name = tmp[0]
        a_type = InternalType.from_string(" ".join(tmp[2:]))
    elif len(tmp) >= 2:
        a_name = tmp[-1]
        a_type = InternalType.from_string(" ".join(tmp[:-1]))
    else:
        a_name = tmp[0]
        a_type = None

    return InternalAttribute(name=a_name, type=a_type, default_value=a_default, visibility=a_visibility)


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
            post_args = post_args.strip()
        except ValueError:
            args = tmp

    try:
        pre_name, f_name = pre_args.rsplit(maxsplit=1)
    except ValueError:
        f_name = pre_args
        pre_name = ""

    f_type = None
    f_visibility = Visibility.PUBLIC
    modifiers = set()

    if pre_name:
        try:
            f_visibility = PLANTUML_VISIBILITY_MATCHER[pre_name[0]]
        except KeyError:
            f_visibility = Visibility.PUBLIC
        else:
            pre_name = pre_name[1::].strip()

        for mod in PLANTUML_FUNCTION_MODIFIER_MATCHER.keys():
            if mod in pre_name:
                modifiers.add(PLANTUML_FUNCTION_MODIFIER_MATCHER[mod])
                pre_name = re.sub(mod, "", pre_name).strip()

        if pre_name:
            # At this point the pre_name can be considered as a return type
            f_type = InternalType.from_string(pre_name)

    arg_list = list()
    if args:
        for arg in args.split(","):
            arg = arg.strip()
            arg_list.append(InternalArgument.from_string(arg))

    return InternalFunction(name=f_name, arguments=arg_list, return_type=f_type, visibility=f_visibility, modifiers=modifiers, extra_elem=post_args)

# TODO: Support Packages

# TODO: Fix the note content that contains lines starting with the Note word
def flatten_string(string: str) -> Tuple[str, Dict[str, str]]:
    ret_str = string

    # Check for namespace separator config
    m = re.search(r"^set namespaceSeparator\s+(\S+)",
                  ret_str, flags=re.MULTILINE)
    if m:
        # Replace the set separator with the default one
        ret_str = re.sub(m.group(1), ".", ret_str)
        # Remove the line that sets the namespace separator
        ret_str = re.sub(r"^set namespaceSeparator.*\s?",
                         "", ret_str,  flags=re.MULTILINE)

    # Removing tabs and extra spaces at the beginning of the lines
    ret_str = re.sub(r"^\s+", "", ret_str, flags=re.MULTILINE)

    # Ensuring that opening brackets are on the same line as the context name
    ret_str = re.sub(r"(.*)\n\s*\{\s*$", r"\1 {", ret_str, flags=re.MULTILINE)
    # Ensuring that the opening bracket is preceded by a whitespace
    ret_str = re.sub(r"(\S)\{", r"\1 {", ret_str, flags=re.MULTILINE)

    # Ensuring that the visibility indicators are separated from the names
    ret_str = re.sub(r"^([\+\-\~\#])(\S)", r"\1 \2",
                     ret_str, flags=re.MULTILINE)

    # Removing multiline comments
    ret_str = re.sub(r"^/'[^']*'/\s?", "", ret_str,
                     flags=re.MULTILINE)
    # Removing single line comments
    ret_str = re.sub(r"^'.*\s?", "", ret_str, flags=re.MULTILINE)

    # TODO: Support single line notes as documentation
    # Removing single line notes
    # Remove the 'note "XXX" as X' type of notes
    ret_str = re.sub(r"^note [^\"]*\"[^\"]+\"\s+as.*\s?", "", ret_str, flags=re.MULTILINE)
    # Remove the 'note X of X : XXX' type of notes
    ret_str = re.sub(r"^note [^\:]*\:[^\:].*\s?", "", ret_str, flags=re.MULTILINE)
    # Separating multiline notes
    tmp_list = ret_str.splitlines()
    ret_list = []
    note_dict = {}
    note_ctx = None
    note_detected = False
    for line in tmp_list:
        if line.lower().startswith("note"):
            note_detected = True
            m = re.search(r"^note\s+\w+\s+of\s+(.*)", line, flags=re.MULTILINE)
            if m:
                note_dict[m.group(1)] = ""
                note_ctx = m.group(1)
            else:
                note_ctx = None
            continue
        elif line.lower().startswith("end note"):
            note_detected = False
            note_ctx = None
            continue
        elif note_detected:
            if note_ctx:
                if note_dict[note_ctx]:
                    note_dict[note_ctx] = "\n".join([note_dict[note_ctx], line])
                else:
                    note_dict[note_ctx] = line
            continue

        ret_list.append(line)

    ret_str = "\n".join(ret_list)

    # Removing Plantuml related elements
    ret_str = re.sub(r"^\@.*\s?", "", ret_str,
                     flags=re.MULTILINE)  # Plantuml anchors
    ret_str = re.sub(r"^\!.*\s?", "", ret_str,
                     flags=re.MULTILINE)  # Plantuml commands

    return ret_str, note_dict


@dataclass
class PlantumlParser(LanguageSpecificParser):
    def translate(self, file: str) -> UnitTranslation:
        with open(file, "r") as f:
            flat_content, note_dict = flatten_string(f.read())
            note_keys = note_dict.keys()
            used_notes = list()
            file_content = flat_content.splitlines()

        unit = UnitTranslation(name=path.splitext(path.basename(file))[0])

        context = [unit]
        # TODO: Keep the line number feature
        for i, line in enumerate(file_content):
            if line != "}":
                pattern = r"({})\s+(\S+)".format("|".join(PLANTUML_CONTEXT_KEYWORDS))
                m = re.match(pattern, line, flags=re.IGNORECASE)
                if m:
                    # Creating the proper context object and adding it to the context list
                    context.append(
                        PLANTUML_CONTEXT_KEYWORDS[m.group(1).lower()](name=m.group(2)))
                    continue
                else:
                    # TODO: support the arrows
                    if [a for a in PLANTUML_ARROWS if a in line]:
                        continue
                    elif "(" not in line:
                        attribute = attribute_from_str(line)
                        log.debug(f"attribute repr: {attribute}")
                        try:
                            context[-1].add_attribute(attribute)
                        except IndexError:
                            log.warn(
                                f"Index problem with the current context: {context}")
                    else:
                        function = function_from_str(line)
                        for k in note_keys:
                            tmp = k
                            #TODO: Ensure that this is not dependant of the note order in the plantuml
                            # Check signature for that
                            if '"' in tmp:
                                m = re.search(r"(\w+)\(", tmp)
                                if m:
                                    tmp = m.group(1)

                            if k not in used_notes and function.name == tmp.rsplit("::", maxsplit=1)[-1]:
                                function.doc = note_dict[k].splitlines()
                                used_notes.append(k)
                                break

                        log.debug(f"function repr: {function}")
                        try:
                            context[-1].add_function(function)
                        except IndexError:
                            log.warn(
                                f"Index problem with the current context: {context}")
                    continue
            else:
                try:
                    if isinstance(context[-1], InternalClass):
                        context[-2].add_class(context[-1])
                    elif isinstance(context[-1], InternalEnum):
                        context[-2].add_enum(context[-1])
                    elif isinstance(context[-1], InternalNamespace):
                        context[-2].add_namespace(context[-1])
                    log.debug(f'end of {context[-1].name}')
                    context.pop()
                    continue
                except IndexError:
                    log.warn(
                        f"Index problem with the current context: {context}")

        return unit

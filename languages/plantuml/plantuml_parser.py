from pathlib import Path
from typing import List
from .plantuml_objects import PlantumlObject
from .plantuml_translationunit import PlantumlTranslationUnit
import re
from rich import print

PATTERN_TO_REMOVE = [
    r"^'.*",  # removing comments
    r"^@startuml.*",
    r"^@enduml.*",
    r"^\!.*"
]

CONTEXT_INDUCING_KEYWORDS = {
    "class": PlantumlObject
}


def format_plantuml_string(string: str) -> List[str]:
    output_lines = []
    string = string.strip()

    # isolating the closing curly braces to better detect contexts
    for symbol in ["{", "}"]:
        if symbol in string:
            string = string.replace(symbol, f"\n{symbol}\n")

    for line in string.splitlines():
        if not line.strip():
            continue
        for pattern in PATTERN_TO_REMOVE:
            line = re.sub(pattern, "", line)

        if line.strip():
            if line.strip() == "{":
                output_lines[-1] += " {"
            else:
                output_lines.append(line.strip())

    return output_lines


def plantuml_file_reader(file_path: Path):
    with file_path.open("r") as f:
        lines = format_plantuml_string(f.read())
        for line in lines:
            yield line


class PlantumlParser:
    @staticmethod
    def parse_file(file_path: Path):

        translation_unit = PlantumlTranslationUnit()

        line_iter = plantuml_file_reader(file_path)
        for line in line_iter:
            for keyword, parser in CONTEXT_INDUCING_KEYWORDS.items():
                if line.startswith(keyword):
                    elem = parser.from_iterator(
                        line_iter, line).to_inter_lang()
                    translation_unit.add(elem)

        return translation_unit

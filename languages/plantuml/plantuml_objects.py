from dataclasses import dataclass
from typing import Iterator
from languages.plantuml.plantuml_variables import PlantumlVariable

from languages.plantuml.plantuml_functions import PlantumlFunction
from intermediate.objects import CodegenObject


@dataclass
class PlantumlObject(CodegenObject):
    @classmethod
    def from_str(cls, string: str):
        name = ""

        obj_elements = {
            "+": {
                "attributes": [],
                "functions": []
            },
            "#": {
                "attributes": [],
                "functions": []
            },
            "-": {
                "attributes": [],
                "functions": []
            }
        }

        # TODO: Rework the extraction of the object body
        object_body = []
        for line in string.splitlines():
            if line.startswith("class"):
                name = line.split()[1]
                continue
            if line.startswith('{'):
                continue
            if line.startswith('}'):
                continue
            object_body.append(line)

        for line in object_body:
            # Checking the visibility of the current line
            # If not found, the visibility is assumed to be public
            try:
                elements = obj_elements[line[0]]
            except KeyError:
                elements = obj_elements["+"]
            else:
                # removing the visibility marker at the beginning
                line = line.lstrip(line[0]).strip()

            if "(" in line:
                # this is a function
                elements["functions"].append(PlantumlFunction.from_str(line))
            else:
                # this is a attribute
                elements["attributes"].append(PlantumlVariable.from_str(line))
        if name:
            return cls(
                name=name,
                public_attributes=obj_elements["+"]["attributes"],
                protected_attributes=obj_elements["#"]["attributes"],
                private_attributes=obj_elements["-"]["attributes"],
                public_functions=obj_elements["+"]["functions"],
                protected_functions=obj_elements["#"]["functions"],
                private_functions=obj_elements["-"]["functions"],
            )

    @classmethod
    def from_inter_lang(cls, elem: CodegenObject):
        return cls(
            elem.name,
            [PlantumlVariable.from_inter_lang(attr)
             for attr in elem.public_attributes],
            [PlantumlVariable.from_inter_lang(attr)
             for attr in elem.protected_attributes],
            [PlantumlVariable.from_inter_lang(attr)
             for attr in elem.private_attributes],
            [PlantumlFunction.from_inter_lang(attr)
             for attr in elem.public_functions],
            [PlantumlFunction.from_inter_lang(attr)
             for attr in elem.protected_functions],
            [PlantumlFunction.from_inter_lang(attr)
             for attr in elem.private_functions]
        )

    @classmethod
    def from_iterator(cls, iterator: Iterator, first_line: str):
        lines = [first_line]

        if "{" in first_line:
            for line in iterator:
                lines.append(line)
                if "}" in line:
                    break

        return PlantumlObject.from_str("\n".join(lines))

    def to_str(self) -> str:
        object_str = f"class {self.name}\n{{\n"

        object_str += str("\n".join([f"+ {attr.to_str()}"
                                     for attr in self.public_attributes])) + "\n"
        object_str += str("\n".join([f"# {attr.to_str()}"
                                     for attr in self.protected_attributes])) + "\n"
        object_str += str("\n".join([f"- {attr.to_str()}"
                                     for attr in self.private_attributes])) + "\n"
        object_str += str("\n".join([f"+ {func.to_str()}"
                                     for func in self.public_functions])) + "\n"
        object_str += str("\n".join([f"# {func.to_str()}"
                                     for func in self.protected_functions])) + "\n"
        object_str += str("\n".join([f"- {func.to_str()}"
                                     for func in self.private_functions])) + "\n"
        object_str += "}"

        return object_str

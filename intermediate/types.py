from dataclasses import dataclass


@dataclass
class CodegenType:
    name: str

    def to_inter_lang(self):
        return CodegenType(self.name)

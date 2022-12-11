from dataclasses import dataclass


class MissingTypeError(Exception):
    pass

@dataclass
class CodegenType:
    name: str

    def to_inter_lang(self):
        return CodegenType(self.name)

from dataclasses import dataclass
from languages.c.c_argument import CArgument


@dataclass
class CVariable(CArgument):

    def to_str(self) -> str:
        return "%s%s" % (super().to_str(), ";")

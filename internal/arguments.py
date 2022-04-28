from dataclasses import dataclass

from internal.types import InternalType


@dataclass
class InternalArgument:
    name: str
    type: InternalType = None
    default_value: str = None

    def __repr__(self) -> str:
        rep_str = f"{self.name}"
        if self.type:
            rep_str = f"{self.type!r} {rep_str}"

        if self.default_value:
            rep_str = f"{rep_str} = {self.default_value}"

        return rep_str

    @classmethod
    def from_string(cls, string: str):
        a_default_value = None
        try:
            string, a_default_value = string.rsplit("=")
            a_default_value = a_default_value.strip()
        except ValueError:
            pass
        finally:
            string = string.strip()

        try:
            a_type, a_name = string.rsplit(maxsplit=1)
        except ValueError:
            a_name = string
            a_type = None

        if a_type:
            a_type = InternalType.from_string(a_type)

        return cls(name=a_name, type=a_type, default_value=a_default_value)

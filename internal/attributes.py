from dataclasses import dataclass

from internal.arguments import InternalArgument
from internal.visibility import Visibility


@dataclass
class InternalAttribute(InternalArgument):
    visibility: Visibility = Visibility.PUBLIC

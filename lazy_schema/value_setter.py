from typing import TYPE_CHECKING, Any, NamedTuple

if TYPE_CHECKING:
    from .schema import Schema


class ValueSetter(NamedTuple):
    schema: "Schema"
    document: dict
    key: str
    a: Any
    b: Any
    exists: bool

    def condition(self):
        return True

    def value(self):
        return self.b

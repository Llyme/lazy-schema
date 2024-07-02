from dataclasses import dataclass
from datetime import datetime, timezone
import json
from typing import TYPE_CHECKING, Any, Callable, Type
from .utils import (
    _field_default,
    _field_condition,
    _field_selector,
)

if TYPE_CHECKING:
    from .schema import Schema


@dataclass(frozen=True)
class Field:
    key: str
    default_value: Callable[["Schema", "Field"], Any]
    """
    Creates a default value.
    """
    selector: Callable[["Schema", "Field", Any], Any]
    """
    Transforms the value.
    """
    condition: Callable[["Schema", "Field", Any], bool]
    """
    Must return `True` to allow setting to this field.
    """
    default: Callable[["Schema", "Field", Any], bool]
    """
    If the default value should be given.
    """
    discrete: bool
    """
    If `False`, it will throw an error if its
    condition is not met.
    """

    @staticmethod
    def __smart_selector(config: dict):
        cast = config.get("cast")

        if cast == "str":
            return lambda s, f, v: str(v)

        if cast == "int":
            return lambda s, f, v: int(v)

        if cast == "float":
            return lambda s, f, v: float(v)

        if cast == "bool":
            return lambda s, f, v: bool(v)

        if cast == "datetime":
            return lambda s, f, v: datetime.fromisoformat(v)

        if cast == "json":
            return lambda s, f, v: json.loads(v)

        return _field_selector

    @staticmethod
    def __smart_default_value(config: dict) -> Any:
        if "default" not in config and "cast" not in config:
            return lambda: config

        cast = config.get("cast")
        default = config.get("default")

        if cast == "datetime":
            if default == "utc_now":
                return lambda: datetime.now(timezone.utc)

            if default == "now":
                return lambda: datetime.now()

        elif cast == "array":
            if default == "empty":
                return lambda: []

        elif cast == "object":
            if default == "empty":
                return lambda: {}

        return lambda: default

    @staticmethod
    def __parse_smart(key: str, config: dict):
        return Field(
            key=key,
            default_value=Field.__smart_default_value(config),
            selector=Field.__smart_selector(config),
            condition=_field_condition,
            default=_field_default,
            discrete=config.get("discrete", False),
        )

    @staticmethod
    def parse(key: str, value):
        if isinstance(value, dict):
            return Field.__parse_smart(key, value)

        default_value = value

        if not callable(value):
            default_value = lambda: value

        return Field(
            key=key,
            default_value=default_value,  # type: ignore
            selector=_field_selector,
            condition=_field_condition,
            default=_field_default,
            discrete=False,
        )

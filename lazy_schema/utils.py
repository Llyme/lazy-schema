from inspect import signature
import json
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    TypeVar,
    Union,
)

if TYPE_CHECKING:
    from .schema import Schema
    from .field import Field

T = TypeVar("T")


def _call(fn: Callable[..., T], *args) -> T:
    """
    Javascript-like function calling.

    Does not care how many arguments are required/given.
    """
    sig = signature(fn)  # type: ignore
    desired_count = len(sig.parameters)
    extra = desired_count - len(args)

    return fn(*args[:desired_count], *[None] * extra)  # type: ignore


def _null_coalesce(*args):
    for arg in args:
        if arg != None:
            return arg

    return None


def _get_pairs(
    args: Iterable[Union[dict, str, None]],
    kwargs: dict,
):
    fields: Dict[str, Any] = {}

    for arg in args:
        if arg == None:
            continue

        if isinstance(arg, str):
            with open(arg, "r") as f:
                json_fields: dict = json.loads(f.read())

                for key, value in json_fields.items():
                    fields[key] = value

        elif isinstance(arg, dict):
            for key, value in arg.items():
                fields[key] = value

    for key, value in kwargs.items():
        fields[key] = value

    return fields


def _field_default(
    schema: "Schema",
    field: "Field",
    value,
):
    if schema.no_default:
        return False

    if schema.discrete and value == None:
        return False

    if schema.no_null and value == None:
        return False

    return True


def _field_condition(
    schema: "Schema",
    field: "Field",
    value,
):
    if schema.no_null and value == None:
        return False

    return True


def _field_selector(
    schema: "Schema",
    field: "Field",
    value,
):
    return value

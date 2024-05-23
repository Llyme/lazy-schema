import json
from typing import Any, NamedTuple, Union, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from schema_pool import SchemaPool


def _null_coalesce(*args):
    for arg in args:
        if arg != None:
            return arg

    return None


class Schema(NamedTuple):
    all_fields: dict
    default_fields: dict
    discrete: bool
    no_default: bool
    no_null: bool

    def __call__(
        self,
        *args: dict,
        __discrete__: bool = None,  # type: ignore
        __no_default__: bool = None,  # type: ignore
        __no_null__: bool = None,  # type: ignore
        **kwargs,
    ) -> dict:
        """
        :__discrete__: When `true`, excludes fields with a `null` default value. Explicitly setting the value to `null` will include it.

        :__no_default__: When `true`, default values are excluded.

        :__no_null__: When `true`, `null` values will never be included.
        """
        fields: Dict[str, Any] = {}

        for arg in args:
            for key in arg:
                fields[key] = arg[key]

        for key in kwargs:
            fields[key] = kwargs[key]

        __discrete__ = _null_coalesce(
            __discrete__,
            fields.get("__discrete__"),
            self.discrete,
        )
        __no_default__ = _null_coalesce(
            __no_default__,
            fields.get("__no_default__"),
            self.no_default,
        )
        __no_null__ = _null_coalesce(
            __no_null__,
            fields.get("__no_null__"),
            self.no_null,
        )

        result = {}

        if not __no_default__:
            for key in self.default_fields:
                value = self.default_fields[key]

                if (__discrete__ or __no_null__) and value == None:
                    continue

                if callable(value):
                    result[key] = value()
                else:
                    result[key] = value

        for key in fields:
            if key.startswith("__") and key.endswith("__"):
                continue

            if key in self.default_fields:
                value = fields[key]

                if not __no_null__ or value != None:
                    result[key] = value
            else:
                raise Exception(f"Key '{key}' does not exist!")

        return result

    def add_to(
        self,
        name: str,
        pool: "SchemaPool",
    ):
        return pool.add_schema(name, self)

    @staticmethod
    def new(
        *args: Union[str, dict],
        __discrete__=False,
        __no_default__=False,
        __no_null__=False,
        **kwargs,
    ):
        """
        :__discrete__: When `true`, excludes fields with a `null` default value. Explicitly setting the value to `null` will include it.

        :__no_default__: When `true`, default values are excluded.

        :__no_null__: When `true`, `null` values will never be included.
        """
        return schema(
            *args,
            __discrete__=__discrete__,
            __no_default__=__no_default__,
            __no_null__=__no_null__,
            **kwargs,
        )


def schema(
    *args: Union[str, dict],
    __discrete__: bool = None,  # type: ignore
    __no_default__: bool = None,  # type: ignore
    __no_null__: bool = None,  # type: ignore
    **kwargs,
):
    """
    :__discrete__: When `true`, excludes fields with a `null` default value. Explicitly setting the value to `null` will include it.

    :__no_default__: When `true`, default values are excluded.

    :__no_null__: When `true`, `null` values will never be included.
    """
    # Get all fields.

    all_fields: dict[str, Any] = {}

    for arg in args:
        if isinstance(arg, str):
            with open(arg, "r") as f:
                json_fields = json.loads(f.read())

                for key in json_fields:
                    all_fields[key] = json_fields[key]

        elif isinstance(arg, dict):
            for key in arg:
                all_fields[key] = arg[key]

    for key in kwargs:
        all_fields[key] = kwargs[key]

    # Get default fields.

    default_fields: dict[str, Any] = {}

    for key in all_fields:
        if key == "__discrete__":
            __discrete__ = _null_coalesce(
                all_fields[key],
                __discrete__,
            )  # type: ignore

        elif key == "__no_default__":
            __no_default__ = _null_coalesce(
                all_fields[key],
                __no_default__,
            )  # type: ignore

        elif key == "__no_null__":
            __no_null__ = _null_coalesce(
                all_fields[key],
                __no_null__,
            )  # type: ignore

        elif key.startswith("__") and key.endswith("__"):
            continue

        else:
            default_fields[key] = all_fields[key]

    # Create generator.

    return Schema(
        all_fields=all_fields,
        default_fields=default_fields,
        discrete=_null_coalesce(
            __discrete__,
            False,
        ),
        no_default=_null_coalesce(
            __no_default__,
            False,
        ),
        no_null=_null_coalesce(
            __no_null__,
            False,
        ),
    )

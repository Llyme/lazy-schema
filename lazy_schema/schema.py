from typing import (
    Any,
    NamedTuple,
    Optional,
    Type,
    Union,
    Dict,
    TYPE_CHECKING,
)
from .value_setter import ValueSetter
from .field import Field
from .utils import _get_pairs, _null_coalesce, _call

if TYPE_CHECKING:
    from .schema_pool import SchemaPool


class Schema(NamedTuple):
    fields: Dict[str, Field]
    discrete: bool
    no_default: bool
    no_null: bool
    value_setter: Type[ValueSetter]
    values: Dict[str, Any] = {}

    def __generate(self):
        result = {}

        for field in self.fields.values():
            value = _call(
                field.default_value,
                self,
                field,
            )

            ok = _call(
                field.default,
                self,
                field,
                value,
            )

            if ok:
                result[field.key] = value

        for key, value in self.values.items():
            if key.startswith("__") and key.endswith("__"):
                continue

            if key not in self.fields:
                raise Exception(f"Key '{key}' does not exist!")

            field = self.fields[key]
            value = _call(
                field.selector,
                self,
                field,
                value,
            )
            setter = self.value_setter(
                schema=self,
                document=result,
                key=key,
                a=result.get(key),
                b=value,
                exists=key in result,
            )

            if not setter.condition():
                continue

            value = setter.value()

            ok = _call(
                field.condition,
                self,
                field,
                value,
            )

            if not ok:
                continue

            if not self.no_null or value != None:
                result[key] = value

        return result

    def __call__(
        self,
        *args: Optional[dict],
        __discrete__: bool = None,  # type: ignore
        __no_default__: bool = None,  # type: ignore
        __no_null__: bool = None,  # type: ignore
        __value_setter__: Type[ValueSetter] = None,  # type: ignore
        **kwargs,
    ) -> dict:
        """
        :__discrete__: When `true`, excludes fields with a `null` default value. Explicitly setting the value to `null` will include it.

        :__no_default__: When `true`, default values are excluded.

        :__no_null__: When `true`, `null` values will never be included.

        :__value_setter: Allows modifying how values are set.
        """
        fields = _get_pairs(args, kwargs)

        __discrete__ = _null_coalesce(
            __discrete__,
            fields.get("__discrete__"),
            self.discrete,
        )  # type: ignore
        __no_default__ = _null_coalesce(
            __no_default__,
            fields.get("__no_default__"),
            self.no_default,
        )  # type: ignore
        __no_null__ = _null_coalesce(
            __no_null__,
            fields.get("__no_null__"),
            self.no_null,
        )  # type: ignore
        __value_setter__ = _null_coalesce(
            __value_setter__,
            fields.get("__value_setter"),
            self.value_setter,
        )  # type: ignore

        return Schema(
            fields=self.fields,
            discrete=__discrete__,
            no_default=__no_default__,
            no_null=__no_null__,
            value_setter=__value_setter__,
            values=fields,
        ).__generate()

    def add_to(
        self,
        name: str,
        pool: "SchemaPool",
    ):
        return pool.add_schema(name, self)


def schema(
    *args: Union[str, dict, None],
    __discrete__: bool = None,  # type: ignore
    __no_default__: bool = None,  # type: ignore
    __no_null__: bool = None,  # type: ignore
    __value_setter__: Type[ValueSetter] = None,  # type: ignore
    **kwargs,
):
    # Get all fields.

    all_fields = _get_pairs(args, kwargs)

    # Get default fields.

    __discrete__ = _null_coalesce(
        all_fields.get("__discrete__"),
        __discrete__,
        False,
    )  # type: ignore
    __no_default__ = _null_coalesce(
        all_fields.get("__no_default__"),
        __no_default__,
        False,
    )  # type: ignore
    __no_null__ = _null_coalesce(
        all_fields.get("__no_null__"),
        __no_null__,
        False,
    )  # type: ignore
    __value_setter__ = _null_coalesce(
        all_fields.get("__value_setter__"),
        __value_setter__,
        ValueSetter,
    )  # type: ignore

    fields = {}

    for key, value in all_fields.items():
        if key.startswith("__") and key.endswith("__"):
            continue

        fields[key] = Field.parse(key, value)

    # Create generator.

    return Schema(
        fields=fields,
        discrete=__discrete__,
        no_default=__no_default__,
        no_null=__no_null__,
        value_setter=__value_setter__,
    )

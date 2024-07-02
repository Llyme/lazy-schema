from .value_setter import ValueSetter
from .schema import Schema, schema
from typing import Type, Union


def _load_document(mongo_collection, query):
    try:
        doc = mongo_collection.find_one(
            query,
            {
                "_id": 0,
            },
        )

        if doc != None:
            return doc
    except:
        pass

    return None


class SchemaPool:
    def __getattr__(self, key: str) -> Schema:
        raise Exception(f"Schema '{key}' does not exist!")

    def __getitem__(self, key: str) -> Schema:
        raise Exception(f"Schema '{key}' does not exist!")

    def pymongo(
        self,
        mongo_collection,
        field_value: str,
        field_name="__name__",
        *args: Union[str, dict, None],
        __discrete__=False,
        __no_default__=False,
        __no_null__=False,
        __value_setter__: Type[ValueSetter] = None,  # type: ignore
        **kwargs,
    ):
        """
        Uses `field_value` as the schema name.
        """

        _schema = self.pymongo_query(
            mongo_collection,
            {
                field_name: field_value,
            },
            *args,
            __discrete__=__discrete__,
            __no_default__=__no_default__,
            __no_null__=__no_null__,
            __value_setter__=__value_setter__,
            **kwargs,
        )

        _schema.add_to(field_value, self)

        return _schema

    def pymongo_query(
        self,
        mongo_collection,
        query,
        *args: Union[str, dict, None],
        __discrete__=False,
        __no_default__=False,
        __no_null__=False,
        __value_setter__: Type[ValueSetter] = None,  # type: ignore
        **kwargs,
    ):
        document = _load_document(mongo_collection, query)

        if document == None:
            raise Exception(
                f"Failed to retrieve schema from MongoDB!",
            )

        return schema(
            document,
            *args,
            __discrete__=__discrete__,
            __no_default__=__no_default__,
            __no_null__=__no_null__,
            __value_setter__=__value_setter__,
            **kwargs,
        )

    def add_schema(
        self,
        name: str,
        schema: Schema,
    ):
        setattr(self, name, schema)

        return schema

    def set(
        self,
        name: str,
        *args: Union[str, dict, None],
        __discrete__=False,
        __no_default__=False,
        __no_null__=False,
        __value_setter__: Type[ValueSetter] = None,  # type: ignore
        **kwargs,
    ):
        return self.add_schema(
            name,
            schema(
                *args,
                __discrete__=__discrete__,
                __no_default__=__no_default__,
                __no_null__=__no_null__,
                __value_setter__=__value_setter__,
                **kwargs,
            ),
        )

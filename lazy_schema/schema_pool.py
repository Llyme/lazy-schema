from .schema import Schema
from typing import Union


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
        *args: Union[str, dict],
        __discrete__=False,
        __no_default__=False,
        __no_null__=False,
        **kwargs,
    ):
        return self.pymongo_query(
            mongo_collection,
            {
                field_name: field_value,
            },
            *args,
            __discrete__=__discrete__,
            __no_default__=__no_default__,
            __no_null__=__no_null__,
            **kwargs,
        )

    def pymongo_query(
        self,
        mongo_collection,
        query,
        *args: Union[str, dict],
        __discrete__=False,
        __no_default__=False,
        __no_null__=False,
        **kwargs,
    ):
        document = _load_document(mongo_collection, query)

        if document == None:
            raise Exception(
                f"Failed to retrieve schema from MongoDB!",
            )

        return Schema.new(
            document,
            *args,
            __discrete__=__discrete__,
            __no_default__=__no_default__,
            __no_null__=__no_null__,
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
        return self.add_schema(
            name,
            Schema.new(
                *args,
                __discrete__=__discrete__,
                __no_default__=__no_default__,
                __no_null__=__no_null__,
                **kwargs,
            ),
        )

# Lazy Schema
Quick and simple schema validator.

# Installation
```
pip install lazy-schema
```

# How to Use

```py
from lazy_schema import schema
from datetime import datetime

exampleSchema = schema(
    stringField="Hello World!",
    numberField=123,
    booleanField=True,
    lambdaField=lambda: datetime.utcnow(),
)

document = exampleSchema(
    stringField="Hi World!",
)

print(document)
```
```
{
    "stringField": "Hi World!",
    "numberField": 123,
    "booleanField": True,
    "lambdaField": [datetime Object]
}
```

## Loading JSON Files
```json
{
    "stringField": "Hi World!",
    "numberField": 123,
    "booleanField": true
}
```
```py
from lazy_schema import schema

exampleSchema = schema(
    "path/to/file.json",
    lambdaField=lambda: datetime.utcnow(),
)

document = exampleSchema(
    stringField="Hi World!",
)

print(document)
```
```
{
    "stringField": "Hi World!",
    "numberField": 123,
    "booleanField": True,
    "lambdaField": [datetime Object]
}
```

## Special Keywords

Field names that are enclosed with double underscores `_`
are special keywords.
They are not included in the schema.

These can be used when creating a schema,
```py
exampleSchema = schema(
    __discrete__=True,
    ...
)
```
inside a schema validation,
```py
document = exampleSchema(
    __discrete__=True,
    ...
)
```
and inside a JSON file.
```json
{
    "__discrete__": true,
    ...
}
```

### \_\_discrete__
Excludes fields with a `None` default value.

```py
from lazy_schema import schema

exampleSchema = schema(
    __discrete__=True,
    fieldA="Hello World!",
    fieldB=None,
    fieldC="Hi World!",
)

document = exampleSchema(
    fieldA=None,
)

print(document)
```
```
{
    "fieldA": None,
    "fieldC": "Hi World!"
}
```

### \_\_no_default__
Default values are not written.

```py
from lazy_schema import schema

exampleSchema = schema(
    __no_default__=True,
    fieldA="Hello World!",
    fieldB=None,
    fieldC="Hi World!",
)

document = exampleSchema(
    fieldA="Hi There!",
)

print(document)
```
```
{
    "fieldA": "Hi There!"
}
```

### \_\_no_null__
`None` values will never be written.

```py
from lazy_schema import schema

exampleSchema = schema(
    __no_null__=True,
    fieldA="Hello World!",
    fieldB=None,
    fieldC="Hi World!",
)

document = exampleSchema(
    fieldA=None,
)

print(document)
```
```
{
    "fieldC": "Hi World!"
}
```

### Comments
Any field names enclosed with double underscores `__name__`
will never be written.

```py
from lazy_schema import schema

exampleSchema = schema(
    __comment__="fieldA should not be None!",
    fieldA="Hello World!",
    __yet_another_comment__="fieldB is always None...",
    fieldB=None,
    __fieldC__="fieldC should always have 'World' in it!",
    fieldC="Hi World!",
)

document = exampleSchema(
    fieldA=None,
)

print(document)
```
```
{
    "fieldA": "Hello World!",
    "fieldB": None,
    "fieldC": "Hi World!"
}
```
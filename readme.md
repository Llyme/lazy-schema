# lazy-schema

A simple schema validation.

## How to Use
```js
import { schema } from 'lazy-schema'

const exampleSchema = schema({
    string: "hi",
    number: 123,
    boolean: true,
    null_value: null
});


let value0 = exampleSchema({
    string: "nice"
});

console.log(value0);

// {
//     string: "nice",
//     number: 123,
//     boolean: true,
//     null_value: null
// }

let value1 = exampleSchema({
    not_in_the_schema: "don't tell me what to do!"
});

// Key 'not_in_the_schema' does not exist!


let value2 = exampleSchema({
    // Default values with `null` will not be added.
    __discrete__: true
});

console.log(value2);

// {
//     string: "hi",
//     number: 123,
//     boolean: true
// }


let value3 = exampleSchema({
    // `null` values will not be added.
    __no_null__: true,
    string: null,
});

console.log(value3);

// {
//     number: 123,
//     boolean: true
// }


let value4 = exampleSchema({
    // Default values will not be added.
    __no_default__: true,
    boolean: false
});

console.log(value4);

// {
//     boolean: false
// }


const example2Schema = schema({
    string: "hi",
    number: 123,
    boolean: true,
    // You can use functions too!
    date_created: () => new Date()
});

let value5 = example2Schema({});

console.log(value5);

// {
//     string: "hi",
//     number: 123,
//     boolean: true,
//     date_created: [Date object]
// }
```

## How to Use: JSON files

You can import `.json` files.

```json
example1.json
{
    "string_value": "hello",
    "number_value": 123,
    "boolean_value": true
}

example2.json
{
    "__double_underscores_are_ignored__": "Just like comments.",
    "__note__": "You can use special keywords here.",
    "__no_null__": true,
    "string_value": "hello",
    "number_value": 123,
    "boolean_value": true,
    "null_value": null
}
```

```js
import { schema } from 'lazy-schema'
import example1JSON from './path/to/example1.json' assert { type: 'json' }
import example2JSON from './path/to/example2.json' assert { type: 'json' }

const example1Schema = schema(example1JSON);

let value1 = example1Schema({});

console.log(value1);

// {
//     string_value: "hello",
//     number_value: 123,
//     boolean_value: true
// }


const example2Schema = schema(example2JSON);

let value2 = example2Schema({});

console.log(value2);

// {
//     string_value: "hello",
//     number_value: 123,
//     boolean_value: true
// }
```
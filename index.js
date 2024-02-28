const SPECIAL_KEYWORDS = {
    "__discrete__": false,
    "__no_default__": false,
    "__no_null__": false,
};

/**
 * __discrete__ = `False`: When `true`,
 * excludes fields with a `null` default value.
 * Explicitly setting the value to `null` will include it.
 * 
 * __no_default__ = `False`: When `true`,
 * default values are excluded.
 * 
 * __no_null__ = `False`: When `true`,
 * `null` values will never be included.
 */
export function schema(...schemas) {
    // Get all fields.
    const ALL_FIELDS = Object.assign({}, ...schemas);

    // Get default fields.

    const DEFAULT_FIELDS = {};

    for (const key in ALL_FIELDS) {
        if (key.startsWith('__') && key.endsWith('__'))
            continue;

        DEFAULT_FIELDS[key] = ALL_FIELDS[key];
    }

    // Create generator.

    return function schema(data = {}) {
        // Get special keywords.
        const special_keywords = {};

        for (const keyword in SPECIAL_KEYWORDS)
            special_keywords[keyword] =
                keyword in data
                    ? data[keyword]
                    : SPECIAL_KEYWORDS[keyword];

        const result = {};

        if (!special_keywords.__no_default__)
            for (const key in DEFAULT_FIELDS) {
                const value = DEFAULT_FIELDS[key];

                const ok =
                    special_keywords.__discrete__ ||
                    special_keywords.__no_null__;

                if (ok && value == null)
                    continue;

                if (typeof (value) === 'function')
                    result[key] = value();
                else
                    result[key] = value;
            }

        for (const key in data) {
            if (key.startsWith('__') && key.endsWith('__'))
                continue;

            if (key in DEFAULT_FIELDS) {
                if (!special_keywords.__no_null__ || data[key] != null)
                    result[key] = data[key];
            } else
                throw `Key '${key}' does not exist!`;
        }

        return result;
    };
}
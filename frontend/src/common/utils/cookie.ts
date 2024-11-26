interface CookieAttributes {
    path?: string;
    domain?: string;
    expires?: number | Date | string; // number: days
}

export default class JSCookie {
    static defaults: CookieAttributes = {};

    public static set(key: string, value: string, attributes: CookieAttributes = {}) {
        attributes = Object.assign({path: '/'}, this.defaults, attributes);

        if (typeof attributes.expires === 'number') {
            const expires = new Date();
            expires.setMilliseconds(expires.getMilliseconds() + attributes.expires * 864e+5);
            attributes.expires = expires;
        }

        // We're using "expires" because "max-age" is not supported by IE
        attributes.expires = attributes.expires ? (attributes.expires as Date).toUTCString() : '';

        try {
            const result = JSON.stringify(value);
            if (/^[{[]/.test(result)) {
                value = result;
            }
        } catch {}

        value = encodeURIComponent(String(value)).replace(/%(23|24|26|2B|3A|3C|3E|3D|2F|3F|40|5B|5D|5E|60|7B|7D|7C)/g, decodeURIComponent);
        key = encodeURIComponent(String(key));
        key = key.replace(/%(23|24|26|2B|5E|60|7C)/g, decodeURIComponent);
        key = key.replace(/[()]/g, escape);

        return (document.cookie = `${key}=${value}${Object.entries(attributes).reduce((p, [key, val]) => p + (val ? (`;${key}${val !== true ? `=${val}` : ''}`) : ''), '')}`);
    }

    public static get(key: string): string | undefined {
        // To prevent the for loop in the first place assign an empty array in case there are no cookies at all.
        // Also prevents odd result when calling "get()"
        const cookies = document.cookie?.split('; ') ?? [];
        const replacements = /(%[0-9A-Z]{2})+/g;

        for (let i = 0; i < cookies.length; i++) {
            const parts = cookies[i].split('=');
            let cookie = parts.slice(1).join('=');

            if (cookie.charAt(0) === '"') {
                cookie = cookie.slice(1, -1);
            }

            try {
                if (parts[0].replace(replacements, decodeURIComponent) === key) {
                    return cookie.replace(replacements, decodeURIComponent);
                }
            } catch {}
        }

        return undefined;
    }

    public static remove(key: string, attributes: CookieAttributes = {}) {
        return this.set(key, '', Object.assign({}, attributes, {expires: -1}));
    }
}

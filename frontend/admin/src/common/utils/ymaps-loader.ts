import ymaps from 'yandex-maps';

interface LoadOptions {
    apikey?: string;
    lang?: string;
    coordorder?: 'latlong' | 'longlat';
    load?: string[];
    mode?: 'release' | 'debug';
    csp?: boolean;
    ns?: string;
    onload?: string;
    onerror?: string;
}

const defaults: LoadOptions = {
    lang: 'ru_RU',
    coordorder: 'longlat'
};

export default {
    load(options: LoadOptions = {}, version = '2.1'): Promise<typeof ymaps> {
        const o = Object.assign({}, defaults, options);
        const params = Object.entries(o).reduce((a, [k, v]) => [...a, `${k}=${encodeURIComponent(v)}`], []).join('&');

        const src = `//api-maps.yandex.ru/${version}/?${params}`;

        if (!this.promise) {
            this.promise = new Promise((resolve, reject) => {
                const scriptElement = document.createElement('script');
                scriptElement.onload = resolve;
                scriptElement.onerror = reject;
                scriptElement.type = 'text/javascript';
                scriptElement.src = src;
                document.body.appendChild(scriptElement);
            }).then(() => new Promise((resolve, reject) => {
                window.ymaps.ready(<() => any> resolve, reject);
            }));
        }

        return this.promise;
    }
};

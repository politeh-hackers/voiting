import {ImageConfig} from './index';

export default class Uploader {
    config: ImageConfig;

    constructor({config}: { config: ImageConfig }) {
        this.config = config;
    }

    uploadSelectedFiles(maxElementCount: number | null, {onPreview, onUpload, onError}: any) {
        const input = document.createElement('input');
        input.type = 'file';
        input.multiple = true;
        input.accept = this.config.types!;
        document.documentElement.appendChild(input);
        input.click();

        input.addEventListener('change', () => {
            let loadedFiles = 0;
            for (const file of Array.from(input.files!)) {
                if (maxElementCount !== null && loadedFiles == maxElementCount) {
                    break;
                } else {
                    loadedFiles++;
                }

                let previewElem = onPreview(file);

                let uploader;

                if (this.config.uploader && typeof this.config.uploader.uploadByFile === 'function') {
                    const customUpload = this.config.uploader.uploadByFile(file);

                    if (!isPromise(customUpload)) {
                        console.warn('Custom uploader method uploadByFile should return a Promise');
                    }

                    uploader = customUpload;
                } else {
                    uploader = this.uploadByFile(file);
                }

                uploader.then((response) => {
                    onUpload(response, previewElem);
                }).catch((error) => {
                    onError(error, previewElem);
                }).finally(() => {
                    document.documentElement.removeChild(input);
                });
            }
        });
    }

    uploadByFile(file: File) {
        const formData = new FormData();

        formData.append(this.config.field!, file);

        if (this.config.additionalRequestData && Object.keys(this.config.additionalRequestData).length) {
            Object.entries(this.config.additionalRequestData).forEach(([name, value]) => {
                formData.append(name, value);
            });
        }

        return fetch(this.config.endpoints!.byFile!, {
            method: 'post',
            body: formData,
            headers: this.config.additionalRequestHeaders
        }).then((response) => response.json());
    }
}

function isPromise(object: any) {
    return object && typeof object.then === 'function';
}

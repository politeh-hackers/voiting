import {BlockTool, BlockToolConstructable, BlockToolConstructorOptions, BlockToolData, ToolboxConfig, ToolConfig} from '@editorjs/editorjs';
import {asImage} from '../../../common/utils/dom';
import UI from './ui';
import ToolboxIcon from './icons/toolbox.svg';
import Uploader from './uploader';
import './index.scss';

export interface ImageConfig extends ToolConfig {
    // Upload endpoints
    endpoints?: {
        // Endpoint for file upload
        byFile?: string
    };
    // Field name for uploaded image
    field?: string;
    // Available mime-types
    types?: string;
    // Any data to send with requests
    additionalRequestData?: Record<string, any>;
    // Allows to pass custom headers with Request
    additionalRequestHeaders?: Record<string, any>;
    // Overrides for Select File button
    buttonContent?: string;
    // Optional custom uploader
    uploader?: {
        // Method that upload image by File
        uploadByFile?: (file: File) => Promise<UploadResponseFormat>
    };
    maxElementCount?: number;
}

export interface ImageGalleryDataFile extends Record<string, any> {
    url: string;
    description: string;
}

export interface ImageGalleryData extends BlockToolData {
    files: ImageGalleryDataFile[];
}

export interface UploadResponseFormat {
    success: number;
    file: { url: string } & Record<string, any>;
}

const ImageGalleryTool: BlockToolConstructable = class ImageGalleryTool implements BlockTool {
    options: BlockToolConstructorOptions<ImageGalleryData, ImageConfig>;
    uploader: Uploader;
    ui: UI;
    _data: ImageGalleryData;

    static get isReadOnlySupported(): boolean {
        return true;
    }

    static get toolbox(): ToolboxConfig {
        return {
            icon: asImage(ToolboxIcon),
            title: 'Gallery'
        };
    }

    constructor(options: BlockToolConstructorOptions<ImageGalleryData, ImageConfig>) {
        this.options = options;

        this.options.config = {
            endpoints: options.config?.endpoints,
            additionalRequestData: options.config?.additionalRequestData || {},
            additionalRequestHeaders: options.config?.additionalRequestHeaders || {},
            field: options.config?.field || 'image',
            types: options.config?.types || 'image/*',
            buttonContent: options.config?.buttonContent || '',
            uploader: options.config?.uploader || undefined,
            tunes: options.config?.tunes || [],
            maxElementCount: options.config?.maxElementCount || undefined
        };

        this.uploader = new Uploader({
            config: this.options.config
        });

        this.ui = new UI({
            api: options.api,
            config: this.options.config,
            onSelectFile: () => {
                let maxElementCount = (this.options.config.maxElementCount) ? this.options.config.maxElementCount - this._data.files.length : null;
                this.uploader.uploadSelectedFiles(maxElementCount, {
                    onPreview: (file: File) => {
                        return this.ui.getPreloader(file);
                    },
                    onUpload: (response: UploadResponseFormat, previewElem: HTMLElement) => {
                        this.onUpload(response, previewElem);
                    },
                    onError: (error: string, previewElem: HTMLElement) => {
                        this.uploadingFailed(error, previewElem);
                    }
                });
            },
            onDeleteFile: (id: number) => {
                this.deleteImage(id);
            },
            onMoveFile: (oldId: number, newId: number) => {
                this.moveImage(oldId, newId);
            },
            readOnly: options.readOnly
        });

        this._data = {} as ImageGalleryData;
        this.data = options.data;
    }

    render() {
        return this.ui.render();
    }

    rendered() {
        this.checkMaxElemCount();

        return this.ui.onRendered();
    }

    validate(savedData: ImageGalleryData) {
        return Boolean(savedData.files && savedData.files.length);
    }

    save() {
        return this.data;
    }

    private appendImage(file: ImageGalleryDataFile) {
        if (file && file.url) {
            if (this.options.config.maxElementCount && this._data.files.length >= this.options.config.maxElementCount) {
                return;
            }

            this._data.files.push(file);
            this.ui.appendImage(file);

            this.checkMaxElemCount();
        }
    }

    private moveImage(from: number, to: number) {
        if (to >= this._data.files.length) {
            to = this._data.files.length - 1;
        }
        this._data.files.splice(to, 0, this._data.files.splice(from, 1)[0]);
    }

    private deleteImage(id: number) {
        if (this._data.files[id] !== undefined) {
            this._data.files.splice(id, 1);

            this.checkMaxElemCount();
        }
    }

    set data(data) {
        this._data.files = [];

        if (data.files) {
            data.files.forEach((file) => {
                this.appendImage(file);
            });
        }
    }

    get data() {
        return this._data;
    }

    onUpload(response: UploadResponseFormat, previewElem: HTMLElement) {
        this.ui.removePreloader(previewElem);
        if (response.success && response.file) {
            this.appendImage({url: response.file.url, description: ''});
        } else {
            this.uploadingFailed('incorrect response: ' + JSON.stringify(response), previewElem);
        }
    }

    uploadingFailed(errorText: string, previewElem: HTMLElement) {
        this.ui.removePreloader(previewElem);

        console.error('Image Tool: uploading failed because of', errorText);

        this.options.api.notifier.show({
            message: this.options.api.i18n.t('Couldn’t upload image. Please try another.'),
            style: 'error'
        });
    }

    checkMaxElemCount() {
        if (this.options.config.maxElementCount && this._data.files.length >= this.options.config.maxElementCount) {
            this.ui.hideFileButton();
        } else {
            this.ui.showFileButton();
        }
    }
};

export default ImageGalleryTool;

import {API} from '@editorjs/editorjs';
import Sortable from 'sortablejs';
import {asImage, createElement} from '../../../common/utils/dom';
import {ImageConfig, ImageGalleryDataFile} from './index';
import buttonIcon from './icons/button-icon.svg';
import trashIcon from './icons/trash.svg';

export interface UiOptions {
    api: API;
    config: ImageConfig;
    onSelectFile: () => void;
    onDeleteFile: (id: number) => void;
    onMoveFile: (oldId: number, newId: number) => void;
    readOnly: boolean;
}

interface UiNodes {
    wrapper: HTMLElement;
    fileButton: HTMLElement;
    container: HTMLElement;
    itemsContainer: HTMLElement;
    controls: HTMLElement;
    preloaderContainer: HTMLElement;
}

export default class UI {
    options: UiOptions;
    nodes: UiNodes;
    preloadersCount: number = 0;
    sortable?: Sortable;

    constructor(options: UiOptions) {
        this.options = options;

        this.nodes = {
            wrapper: createElement('div', {class: [this.CSS.baseClass, this.CSS.wrapper]}),
            fileButton: this.createFileButton(),
            container: createElement('div', {class: this.CSS.container}),
            itemsContainer: createElement('div', {class: this.CSS.itemsContainer}),
            controls: createElement('div', {class: this.CSS.controls}),
            preloaderContainer: createElement('div', {class: this.CSS.preloaderContainer})
        };

        /**
         * Create base structure
         *  <wrapper>
         *    <container>
         *      <items-container>
         *        <image-container />
         *      </items-container>
         *      <controls>
         *        <preloader-container />
         *        <select-file-button />
         *      </controls>
         *    </container>
         *  </wrapper>
         */
        this.nodes.controls.appendChild(this.nodes.preloaderContainer);
        this.nodes.controls.appendChild(this.nodes.fileButton);

        this.nodes.container.appendChild(this.nodes.itemsContainer);
        this.nodes.container.appendChild(this.nodes.controls);

        this.nodes.wrapper.appendChild(this.nodes.container);

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            this.nodes.itemsContainer.addEventListener(eventName, function (e) {
                e.preventDefault();
                e.stopPropagation();
            }, false);
        });
    }

    get CSS() {
        return {
            baseClass: this.options.api.styles.block,
            loading: this.options.api.styles.loader,
            input: this.options.api.styles.input,
            button: this.options.api.styles.button,

            wrapper: 'image-gallery',
            container: 'image-gallery__container',
            controls: 'image-gallery__controls',
            itemsContainer: 'image-gallery__items',
            imageContainer: 'image-gallery__image',
            preloaderContainer: 'image-gallery__preloaders',
            imagePreloader: 'image-gallery__preloader',
            imageEl: 'image-gallery__image-picture',
            trashButton: 'image-gallery__image-trash'
        };
    };

    static get status() {
        return {
            EMPTY: 'empty',
            UPLOADING: 'loading',
            FILLED: 'filled'
        };
    }

    render() {
        return this.nodes.wrapper;
    }

    onRendered() {
        if (!this.sortable) {
            this.sortable = new Sortable(this.nodes.itemsContainer, {
                handle: `.${this.CSS.imageContainer}`,
                filter: `.${this.CSS.trashButton}`,
                onStart: () => {
                    this.nodes.itemsContainer.classList.add(`${this.CSS.itemsContainer}--drag`);
                },
                onEnd: (evt) => {
                    this.nodes.itemsContainer.classList.remove(`${this.CSS.itemsContainer}--drag`);

                    if (evt.oldIndex !== evt.newIndex) {
                        this.options.onMoveFile(evt.oldIndex!, evt.newIndex!);
                    }
                }
            });
        }
    }

    createFileButton() {
        const button = createElement('div', {class: this.CSS.button});

        button.innerHTML = this.options.config.buttonContent || `${asImage(buttonIcon)} ${this.options.api.i18n.t('Add images')}`;

        button.addEventListener('click', () => {
            this.options.onSelectFile();
        });

        return button;
    }

    showFileButton() {
        this.nodes.fileButton.style.display = '';
    }

    hideFileButton() {
        this.nodes.fileButton.style.display = 'none';
    }

    getPreloader(file: File) {
        let preloader = createElement('div', {class: this.CSS.imagePreloader});

        this.nodes.preloaderContainer.append(preloader);

        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = (e) => {
            preloader.style.backgroundImage = `url(${e.target!.result})`;
        };

        return preloader;
    }

    removePreloader(preloader: HTMLElement) {
        preloader.remove();
    }

    appendImage(file: ImageGalleryDataFile) {
        let url = file.url;

        const tag: keyof HTMLElementTagNameMap = /\.mp4$/.test(url) ? 'video' : 'img';

        const attributes: Record<string, any> = {
            src: url,
            loading: "lazy",
        };

        let eventName = 'load';

        if (tag === 'video') {
            attributes.autoplay = false;
            attributes.muted = true;
            attributes.playsinline = true;

            eventName = 'loadeddata';
        }

        let imageContainer = createElement('div', {class: this.CSS.imageContainer});
        let imageEl = createElement(tag, {class: this.CSS.imageEl, attributes});

        imageEl.addEventListener(eventName, () => {
            this.toggleStatus(imageContainer, UI.status.FILLED);
        });

        imageContainer.appendChild(imageEl);

        const title = this.options.api.i18n.t('Delete');

        let imageTrash = createElement('div', {
            class: this.CSS.trashButton, attributes: {
                innerHTML: asImage(trashIcon),
                title
            }
        });

        this.options.api.tooltip.onHover(imageTrash, title, {
            placement: 'top'
        });

        imageTrash.addEventListener('click', () => {
            this.options.api.tooltip.hide();

            let arrayChild = Array.prototype.slice.call(this.nodes.itemsContainer.children);
            let elIndex = arrayChild.indexOf(imageContainer);

            if (elIndex !== -1) {
                this.nodes.itemsContainer.removeChild(imageContainer);

                this.options.onDeleteFile(elIndex);
            }
        });

        imageContainer.appendChild(imageTrash);

        const description = createElement('input', {
            class: this.CSS.input,
            attributes: {
                name: 'description',
                value: file.description || '',
                placeholder: this.options.api.i18n.t('Caption')
            }
        });

        description.addEventListener('dragstart', (event) => {
            event.preventDefault();
        });

        description.addEventListener('input', () => {
            file.description = description.value;
        });

        imageContainer.appendChild(description);

        this.nodes.itemsContainer.append(imageContainer);
    }

    toggleStatus(elem: HTMLElement, status: string) {
        for (const it of Object.values(UI.status)) {
            elem.classList.toggle(`${this.CSS.imageContainer}--${it}`, status === it);
        }
    }
}

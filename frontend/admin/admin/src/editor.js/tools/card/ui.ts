import {createElement} from '../../../common/utils/dom';
import Modal from '../../../common/components/modal';
import {CardTool, CardType} from './index';

export default class UI {
    private owner: CardTool;
    private types: Record<CardType, string>;

    private $_wrapper?: HTMLElement;
    private $_placeholder?: HTMLElement;
    private $_selector?: HTMLElement;
    private $_selectorView?: HTMLElement;
    private _modal?: Modal;

    private _type: CardType = 'person';
    private _search: string = '';

    constructor(owner: CardTool, types: Record<CardType, string>) {
        this.owner = owner;
        this.types = types;
    }

    get $placeholder() {
        if (!this.$_placeholder) {
            this.$_placeholder = createElement('div', {
                class: [this.owner.options.api.styles.button, 'card-placeholder'],
                attributes: {
                    innerText: this.owner.options.api.i18n.t('Select')
                }
            });

            this._modal = new Modal(this.owner.options.api.i18n.t('Select card'), this.$selector);
            this.$_placeholder.addEventListener('click', () => {
                this._modal.show();
            });
        }

        return this.$_placeholder;
    }

    get $wrapper() {
        return this.$_wrapper ??= createElement('div', {
            class: [this.owner.options.api.styles.block, 'editor-card']
        });
    }

    get $selector() {
        if (!this.$_selector) {
            this.$_selector = createElement('div', {class: 'card-selector'}, {}, [
                createElement('div', {class: 'card-selector-type'}, {}, Object.entries(this.types).map(([type, name]) => {
                    return createElement('div', {class: 'card-selector-type-check'}, {}, [
                        createElement('input', {
                            attributes: {
                                checked: this._type === type,
                                id: `card_selector_${type}`,
                                type: 'radio',
                                name: 'card-selector-type',
                                value: type
                            }
                        }, {
                            change: () => {
                                this._type = type as CardType;
                                this.loadCardList();
                            }
                        }),
                        createElement('label', {attributes: {'for': `card_selector_${type}`, innerText: name}})
                    ]);
                })),
                createElement('input', {
                    class: [this.owner.options.api.styles.input, 'card-selector-filter'],
                    attributes: {
                        placeholder: this.owner.options.api.i18n.t('Search')
                    }
                }, {
                    input: (e) => {
                        this._search = (e.target as HTMLInputElement).value;
                        this.loadCardList();
                    }
                }),
                (this.$_selectorView = createElement('div', {class: 'card-selector-view'}))
            ]);
        }

        return this.$_selector;
    }

    private loadCardList() {
        this.$_selector.classList.add('loading');
        fetch(this.owner.options.config.cardListUrl(this._type, this._search)).then((response) => {
            return response.text();
        }).then((data) => {
            this.$_selectorView.innerHTML = data;
            this.$_selectorView.querySelectorAll<HTMLElement>('.card-item').forEach((item) => {
                item.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.owner.options.data = {type: this._type, id: parseInt(item.dataset.id)};
                    this.owner.options.block.dispatchChange();
                    this.render();
                    this._modal.close();
                });
            });
        }).finally(() => {
            this.$_selector.classList.remove('loading');
        });
    }

    private loadCard() {
        return fetch(this.owner.options.config.cardUrl(this.owner.options.data)).then((response) => response.text());
    }

    public render() {
        if (!this.owner.options.data.id) {
            this.$wrapper.appendChild(this.$placeholder);
            this._modal.show();
            this.loadCardList();
        } else {
            this.loadCard().then((content) => {
                this.$wrapper.innerHTML = content;
            });
        }

        return this.$wrapper;
    }
}

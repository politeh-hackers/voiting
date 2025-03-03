import {createElement} from '../../../common/utils/dom';
import './style.scss';

export default class Modal {
    $wrapper: HTMLElement;
    $modal: HTMLElement;

    constructor(title: string, $content: HTMLElement) {
        this.$wrapper = createElement('div', {
            class: 'x-modal-wrapper'
        }, {
            click: (e) => {
                if (e.target === this.$wrapper) {
                    this.close();
                }
            },
            transitionend: (e) => {
                if (!this.$wrapper.classList.contains('show')) {
                    if (e.target === this.$wrapper && (e as TransitionEvent).propertyName === 'opacity') {
                        document.documentElement.removeChild(this.$wrapper);
                    }
                }
            }
        }, [
            this.$modal = createElement('div', {class: 'x-modal-container'}, {}, [
                // header
                createElement('div', {class: 'x-modal-header'}, {}, [
                    createElement('span', {class: 'x-modal-title', attributes: {innerText: title}}),
                    createElement('div', {class: 'x-modal-close-button'}, {click: () => this.close()})
                ]),

                // content
                createElement('div', {class: 'x-modal-content'}, {}, [
                    $content
                ])
            ])
        ]);
    }

    public show(): Modal {
        document.documentElement.appendChild(this.$wrapper);
        setTimeout(() => this.$wrapper.classList.add('show'), 0);
        return this;
    }

    public close(): Modal {
        this.$wrapper.classList.remove('show');
        return this;
    }
}

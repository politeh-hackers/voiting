import {BlockTool, BlockToolConstructable, BlockToolConstructorOptions, BlockToolData, ToolboxConfig} from '@editorjs/editorjs';
import {asImage} from '../../../common/utils/dom';
import ToolboxIcon from './icons/toolbox.svg';
import UI from './ui';
import './style.scss';

export type CardType = 'person' | 'band' | 'artist' | 'partner' | 'event' | 'news' | 'info_page';

export interface CardToolData extends BlockToolData {
    type: CardType;
    id: number;
}

export interface CardToolConfig {
    cardListUrl: (type: CardType, search: string) => string;
    cardUrl: (data: CardToolData) => string;
}

export class CardTool implements BlockTool {
    options: BlockToolConstructorOptions<CardToolData, CardToolConfig>;
    private ui: UI;

    static get types() {
        return {
            'person': 'Личность',
            'partner': 'Партнер',
            'artist': 'Артист',
            'band': 'Коллектив',
            'event': 'Мероприятие',
            'news': 'Новость',
            'info_page': 'Информация',
            'product': 'Товары',
            'service': 'Услуги',
        };
    }

    constructor(options: BlockToolConstructorOptions<CardToolData, CardToolConfig>) {
        if (typeof options.config.cardListUrl !== 'function') {
            throw new Error('CartToolConfig.cardListUrl option muset be function and set');
        }

        this.options = options;

        this.ui = new UI(this, CardTool.types);
    }

    static get toolbox(): ToolboxConfig {
        return {
            icon: asImage(ToolboxIcon),
            title: 'Card'
        };
    }

    public validate(data: CardToolData) {
        return Boolean(data.type && data.id);
    }

    public render() {
        return this.ui.render();
    }

    public save(_: HTMLElement) {
        return this.options.data;
    }
}

export default CardTool as BlockToolConstructable;

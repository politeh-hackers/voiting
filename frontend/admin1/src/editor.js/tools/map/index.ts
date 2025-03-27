import {
    BlockTool,
    BlockToolConstructable,
    BlockToolConstructorOptions,
    BlockToolData,
    ToolboxConfig
} from '@editorjs/editorjs';
import {asImage} from '../../../common/utils/dom';
import ToolboxIcon from './icons/toolbox.svg';
import UI from './ui';
import './style.scss';

export interface MapToolData extends BlockToolData {
    points: Array<{ coordinates: [number, number], caption?: string }>;
    caption?: string;
}

export interface MapToolConfig {
    center: [number, number];
    zoom: number;
}

export class MapTool implements BlockTool {
    options: BlockToolConstructorOptions<MapToolData, MapToolConfig>;
    private ui: UI;

    constructor(options: BlockToolConstructorOptions<MapToolData, MapToolConfig>) {
        this.options = options;
        this.options.config.zoom ??= 16;

        this.ui = new UI(this);
    }

    static get toolbox(): ToolboxConfig {
        return {
            icon: asImage(ToolboxIcon),
            title: 'Map'
        };
    }

    public validate(data: MapToolData) {
        return Boolean(data.points && data.points.length);
    }

    public render() {
        return this.ui.render();
    }

    public save(_) {
        return this.options.data;
    }
}

export default MapTool as BlockToolConstructable;

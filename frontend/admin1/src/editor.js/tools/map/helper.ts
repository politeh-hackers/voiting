import ymaps, {geometry, IEvent, IPlacemarkOptions} from 'yandex-maps';
import YMLoader from '../../../common/utils/ymaps-loader';

export type PointCoordinates = [number, number];
export type BoxCoordinates = [PointCoordinates, PointCoordinates];

export interface MapParams {
    bounds?: BoxCoordinates;
    center?: PointCoordinates;
    zoom?: number;
}

export type YMaps = typeof ymaps;

export default class YMHelper {
    static ymaps: YMaps;

    static init($element: HTMLElement, params: MapParams) {
        return YMLoader.load().then((ymaps) => {
            this.ymaps = ymaps;

            const map = new ymaps.Map($element, {
                controls: [
                    new ymaps.control.ZoomControl({options: {position: {right: 10, top: 43}}}),
                    // new ymaps.control.FullscreenControl({options: {position: {right: 10, top: 10}}}),
                    // @ts-ignore
                    // new ymaps.control.TypeSelector({options: {position: {right: 44, top: 10}}})
                ],
                ...params
            }, {
                // avoidFractionalZoom: true,
                autoFitToViewport: 'always',
                restrictMapArea: [[-Infinity, -85], [Infinity, 85]],
                nativeFullscreen: true,
                // suppressMapOpenBlock: true,
                // copyrightLogoVisible: false,
                copyrightProvidersVisible: false,
                copyrightUaVisible: false
            });

            const cpane = $element.querySelector('[class*="-copyrights-pane"]');
            cpane?.parentElement.removeChild(cpane);

            return map;
        });
    }

    static getIconOptions() {
        return {
            preset: 'islands#greenDotIconWithCaption',
            iconLayout: 'default#image',
            iconImageHref: '/static/images/etc/yandex-map-style-point.svg',
            iconImageSize: [26, 32]
        } as ymaps.IPlacemarkOptions;
    }

    static placemark(
        position: PointCoordinates,
        properties = {},
        options: IPlacemarkOptions = {
        },
        events: Partial<Record<keyof GlobalEventHandlersEventMap, (event: IEvent<DragEvent, geometry.Point>) => void>> = {}
    ) {
        const placemark = new this.ymaps.Placemark(position, properties, {
            ...this.getIconOptions(),
            ...options
        } as ymaps.IPlacemarkOptions);
        for (const [event, fn] of Object.entries(events)) {
            placemark.events.add(event, fn);
        }
        return placemark;
    }
}

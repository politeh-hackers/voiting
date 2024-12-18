import ymaps from 'yandex-maps';
import {createElement} from '../../../common/utils/dom';
import {MapTool} from '../../../editor.js/tools/map';
import YMHelper from '../../../editor.js/tools/map/helper';


export default class UI {
    private owner: MapTool;

    private $wrapper: HTMLElement;
    private $map: HTMLElement;
    private _map: ymaps.Map;

    constructor(owner: MapTool) {
        this.owner = owner;
        this.owner.options.data.points = this.owner.options.data.points || [];
    }

    render() {
        if (!this.$wrapper) {
            this.$wrapper = createElement('div', {class: [this.owner.options.api.styles.block, 'map-block-wrapper']}, {}, [
                this.$map = createElement('div', {class: 'map-block'}),
                createElement('input', {
                    class: this.owner.options.api.styles.input,
                    attributes: {
                        value: this.owner.options.data.caption || '',
                        placeholder: this.owner.options.api.i18n.t('Caption')
                    }
                }, {
                    input: (e) => {
                        this.owner.options.data.caption = (e.target as HTMLInputElement).value;
                        this.owner.options.block.dispatchChange();
                    }
                })
            ]);

            const location = this.owner.options.data.points?.[0]?.coordinates || this.owner.options.config.center;

            YMHelper.init(this.$map, {
                center: location,
                zoom: this.owner.options.config.zoom
            }).then((map) => {
                this._map = map;
                this._map.behaviors.disable('scrollZoom');

                const geoObjects = [];

                const removePointAtIndex = (points: any[], index: number) => {
                    points.splice(index, 1);
                    this.owner.options.block.dispatchChange();
                };

                const pointIndex = (p: any) => {
                    return this.owner.options.data.points.findIndex((point) => point.coordinates === p.coordinates);
                };

                const createPointMark = (coordinates: [number, number]) => {
                    return YMHelper.placemark(coordinates, {}, {draggable: true}, {
                        dragend: (e) => {
                            const location = e.originalEvent.target.geometry.getCoordinates();
                            this._map.panTo(location, {flying: true});

                            const index = pointIndex({coordinates});
                            if (index !== -1) {
                                this.owner.options.data.points[index].coordinates = location as [number, number];
                                this.owner.options.block.dispatchChange();
                            }
                        }
                    });
                };

                const addPoint = (coordinates: [number, number]) => {
                    const mark = createPointMark(coordinates);

                    mark.events.add('click', () => {
                        this._map.geoObjects.remove(mark);
                        const index = pointIndex({coordinates: mark.geometry.getCoordinates()});
                        if (index !== -1) {
                            removePointAtIndex(this.owner.options.data.points, index);
                        }
                    });

                    mark.properties.set('iconCaption', '');

                    this._map.geoObjects.add(mark);

                    this.owner.options.data.points.push({coordinates});
                    this.owner.options.block.dispatchChange();
                };

                this.owner.options.data.points?.forEach((point) => {
                    const mark = createPointMark(point.coordinates);

                    mark.events.add('click', () => {
                        this._map.geoObjects.remove(mark);
                        const index = pointIndex(point);
                        if (index !== -1) {
                            removePointAtIndex(this.owner.options.data.points, index);
                        }
                    });

                    mark.properties.set('iconCaption', point.caption || '');
                    this._map.geoObjects.add(mark);
                    geoObjects.push(mark)
                });

                this._map.events.add('click', (e) => {
                    const location = e.get('coords');
                    addPoint(location as [number, number]);
                });

                if (this._map.geoObjects.getLength() > 1) {
                    this._map.setBounds(this._map.geoObjects.getBounds(), {checkZoomRange: true, zoomMargin: [35]});
                }

            });
        }

        return this.$wrapper;
    }
}

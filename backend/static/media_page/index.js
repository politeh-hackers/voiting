export function initializeMap(mapId, coordinates, caption) {
    // Объединяем долготу и широту
    const longitude = [coordinates[0], coordinates[1]].join('.'); // Объединяем долготу
    const latitude = [coordinates[2], coordinates[3]].join('.'); // Объединяем широту
    // Преобразуем в числа
    const coordinatesFinal = [parseFloat(latitude), parseFloat(longitude)];
    console.log(longitude, latitude);
    ymaps.ready(() => {
        const map = new ymaps.Map(mapId, {
            center: coordinatesFinal,
            zoom: 14,
            controls: []
        });
        map.behaviors.disable(['scrollZoom', 'drag', 'dblClickZoom', 'rightMouseButtonMagnifier', 'multiTouch']);
        map.options.set('theme', 'dark'); // Настройка цветовой схемы (серая)
        const placemark = new ymaps.Placemark(coordinatesFinal, {
            hintContent: caption
        });
        map.geoObjects.add(placemark);
        window.addEventListener('resize', () => {
            map.container.fitToViewport();
        });
    });
}
// Инициализация галереи
const initGallery = () => {
    const swiper = new Swiper('.swiper-container', {
        loop: true,
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
    });
};
document.addEventListener('DOMContentLoaded', () => {
    initGallery();
});

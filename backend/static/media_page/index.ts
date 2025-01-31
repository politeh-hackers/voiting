declare var Swiper: any;
declare var ymaps: any;

const initGallery = (): void => {
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

export function initializeMap(mapId: string, coordinates: [number, number], caption: string) {
    // Ждем загрузки Yandex Maps API
    ymaps.ready(function () {
        var map = new ymaps.Map(mapId, {
            center: [coordinates[1], coordinates[0]], // Координаты [широта, долгота]
            zoom: 14
        });
        
        var placemark = new ymaps.Placemark([coordinates[1], coordinates[0]], {
            hintContent: caption
        });
        
        map.geoObjects.add(placemark);
    });
}

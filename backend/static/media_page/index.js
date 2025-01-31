"use strict";

var initGallery = function () {
    var swiper = new Swiper('.swiper-container', {
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
document.addEventListener('DOMContentLoaded', function () {
    initGallery();
});
export function initializeMap(mapId, coordinates, caption) {
    var longitude = [coordinates[0], coordinates[1]].join('.');  // Объединяем долготу
    var latitude = [coordinates[2], coordinates[3]].join('.');    // Объединяем широту
    var coordinatesFinal = [parseFloat(latitude), parseFloat(longitude)];
    console.log(longitude , latitude)
    ymaps.ready(function () {
        var map = new ymaps.Map(mapId, {
            center: coordinatesFinal,
            zoom: 14,
            controls: []
        });
        map.behaviors.disable(['scrollZoom', 'drag', 'dblClickZoom', 'rightMouseButtonMagnifier', 'multiTouch']);

        map.options.set('theme', 'dark'); // Настройка цветовой схемы (серая)

        var placemark = new ymaps.Placemark(coordinatesFinal, {
            hintContent: caption
        });
        map.geoObjects.add(placemark);
    });
}

function initMap() {
    console.log("Map initialized");
    var mapContainer = document.getElementById('map1');
    var map = new ymaps.Map('map1', {
        center: [55.200000, 30.250000],
        zoom: 14,
        controls: []
    });
    // Функция для обновления размеров карты
    var updateMapSize = function () {
        if (mapContainer) {
            // Перерасчет размеров карты при изменении размеров контейнера
            map.container.fitToViewport();
        }
    };
    // Инициализируем карту с начальным размером
    updateMapSize();
    // Обработчик изменения размеров окна
    window.addEventListener("resize", function () {
        updateMapSize();
    });
    // Используем ResizeObserver для отслеживания изменений размеров контейнера карты
    var resizeObserver = new ResizeObserver(function () {
        updateMapSize();
    });
    resizeObserver.observe(mapContainer);
    // Отключаем возможность перемещения карты
    map.behaviors.disable('drag');
    // Отключаем возможность масштабирования колесом мыши
    map.behaviors.disable('scrollZoom');
    // Отключаем возможность использования двойного клика для масштабирования
    map.behaviors.disable('dblClickZoom');
    // Отключаем возможность использования клавиш для перемещения
    map.behaviors.disable('keyboard');
    var coordinates = [
        [55.199440, 30.225416],
        [55.194158, 30.229461],
        [55.197758, 30.266929],
        [55.208433, 30.271005],
        [55.208408, 30.243153]
    ];
    var polygon = new ymaps.Polygon([coordinates], {}, {
        fillColor: '#FF000033',
        strokeColor: '#FF0000',
        strokeWidth: 2
    });
    map.geoObjects.add(polygon);
    // Создаем маркер
    var marker = new ymaps.Placemark([55.197414, 30.234178], {
        iconLayout: 'default#image',
        iconImageHref: 'D:/voiting/backend/static/map/location-dot.svg'
    });
    map.geoObjects.add(marker);
}
ymaps.ready(initMap);

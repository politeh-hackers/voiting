export function initializeMap(mapId: string, coordinates: [string, string, string, string], caption: string) {
    // Преобразуем строки в числа
    const numericCoordinates = coordinates.map(coord => parseFloat(coord));

    // Ждем загрузки Yandex Maps API
    ymaps.ready(function () {
        var map = new ymaps.Map(mapId, {
            center: [numericCoordinates[2], numericCoordinates[3]], // Координаты [широта, долгота]
            zoom: 14
        });
        
        // Преобразуем строку в массив дробных чисел
        const combinedCoordinates = [
            numericCoordinates[0], // Первые координаты
            numericCoordinates[1]  // Вторые координаты
        ];

        console.log(combinedCoordinates); // Выводим объединенные координаты в консоль

        var placemark = new ymaps.Placemark(combinedCoordinates, {
            hintContent: caption
        });
        
        map.geoObjects.add(placemark);
    });
} 
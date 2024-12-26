declare var ymaps: any; // Для TypeScript

function initMap(): void {
    // Создаем карту
    const map = new ymaps.Map('map', {
        center: [55.200000, 30.250000], // Координаты центра карты
        zoom: 10, // Масштаб
    });

    const coordinates = [
        [55.199440, 30.225416],
        [55.194158, 30.229461],
        [55.197758, 30.266929],
        [55.208433, 30.271005],
        [55.208408, 30.243153]
    ];

    const polygon = new ymaps.Polygon([coordinates], {}, {
        fillColor: '#6699FF33', // Цвет заливки
        strokeColor: '#0000FF', // Цвет обводки
        strokeWidth: 2
    });
    map.geoObjects.add(polygon);

    // Создаем маркер
    const marker = new ymaps.Placemark([55.199440, 30.225416], {
        hintContent: 'Перетащи меня!'
    });
    map.geoObjects.add(marker);
    marker.options.set('draggable', true); // Сделаем маркер перетаскиваемым

    // Переменная для хранения последней допустимой позиции маркера
    let lastValidPosition: number[] = [55.199440, 30.225416];

    // Функция для проверки, внутри ли маркер в полигоне
    function isMarkerInPolygon(): boolean {
        const position: number[] = marker.geometry.getCoordinates();
        return polygon.geometry.contains(position);
    }

    // Функция для отправки координат и данных формы на сервер через POST-запрос
    async function sendDataToServer(data: any): Promise<void> {
        try {
            const response = await fetch('http://127.0.0.1:8000/appeals/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data) // Отправляем данные как JSON
            });

            if (response.ok) {
                console.log('Данные успешно отправлены');
            } else {
                console.error('Ошибка при отправке данных');
            }
        } catch (error) {
            console.error('Ошибка сети:', error);
        }
    }

    // Отслеживаем перемещение маркера
    marker.events.add('drag', function () {
        // Получаем текущие координаты маркера
        const position: number[] = marker.geometry.getCoordinates();

        // Если маркер выходит за пределы полигона
        if (!isMarkerInPolygon()) {
            // Возвращаем маркер в последнюю допустимую позицию
            marker.geometry.setCoordinates(lastValidPosition);
        } else {
            // Если маркер внутри полигона, обновляем последнюю допустимую позицию
            lastValidPosition = position;
        }
    });

    // Обработчик нажатия кнопки "Сохранить"
    const saveButton = document.getElementById('saveBtn');
    if (saveButton) {
        saveButton.addEventListener('click', function () {
            // Проверяем, внутри ли маркер в полигоне перед отправкой данных
            if (isMarkerInPolygon()) {
                const position = marker.geometry.getCoordinates();
                
                // Собираем данные из формы
                const formData = new FormData(document.getElementById('appealForm') as HTMLFormElement);
                const appealData = {
                    location: position,
                    last_name: formData.get('last_name'),
                    first_name: formData.get('first_name'),
                    patronymic: formData.get('patronymic'),
                    phone: formData.get('phone'),
                    text: formData.get('text'),
                    photos: formData.getAll('photos') // Получаем все выбранные файлы
                };

                // Отправляем данные на сервер
                sendDataToServer(appealData);
            } else {
                alert('Маркер находится вне полигона. Переместите его внутрь полигона перед сохранением.');
            }
        });
    }
}

// Убедимся, что API загружено и готово к использованию
ymaps.ready(initMap);

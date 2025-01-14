"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
console.log("dddddddd");
function initMap() {
    console.log("dddddddd");
    const map = new ymaps.Map('map', {
        center: [55.200000, 30.250000],
        zoom: 10,
    });
    const coordinates = [
        [55.199440, 30.225416],
        [55.194158, 30.229461],
        [55.197758, 30.266929],
        [55.208433, 30.271005],
        [55.208408, 30.243153]
    ];
    const polygon = new ymaps.Polygon([coordinates], {}, {
        fillColor: '#6699FF33',
        strokeColor: '#0000FF',
        strokeWidth: 2
    });
    map.geoObjects.add(polygon);
    // Создаем маркер
    const marker = new ymaps.Placemark([55.199440, 30.225416], {
        hintContent: 'Перетащи меня!'
    });
    map.geoObjects.add(marker);
    marker.options.set('draggable', true);
    let lastValidPosition = [55.199440, 30.225416];
    function isMarkerInPolygon() {
        const position = marker.geometry.getCoordinates();
        return polygon.geometry.contains(position);
    }
    function sendDataToServer(data) {
        return __awaiter(this, void 0, void 0, function* () {
            try {
                const response = yield fetch('http://127.0.0.1:8000/appeals/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                if (response.ok) {
                    console.log('Данные успешно отправлены');
                }
                else {
                    console.error('Ошибка при отправке данных');
                }
            }
            catch (error) {
                console.error('Ошибка сети:', error);
            }
        });
    }
    marker.events.add('drag', function () {
        const position = marker.geometry.getCoordinates();
        if (!isMarkerInPolygon()) {
            marker.geometry.setCoordinates(lastValidPosition);
        }
        else {
            lastValidPosition = position;
        }
    });
    const saveButton = document.getElementById('saveBtn');
    if (saveButton) {
        saveButton.addEventListener('click', function () {
            if (isMarkerInPolygon()) {
                const position = marker.geometry.getCoordinates();
                const formData = new FormData(document.getElementById('appealForm'));
                const appealData = {
                    location: position,
                    last_name: formData.get('last_name'),
                    first_name: formData.get('first_name'),
                    patronymic: formData.get('patronymic'),
                    phone: formData.get('phone'),
                    text: formData.get('text'),
                    photos: formData.getAll('photos')
                };
                sendDataToServer(appealData);
            }
            else {
                alert('Маркер находится вне полигона. Переместите его внутрь полигона перед сохранением.');
            }
        });
    }
}
const searchButton = document.getElementById('searchButton');
const searchPopup = document.getElementById('searchPopup');
let isActive = false;
// Проверка на существование элементов
if (searchButton && searchPopup) {
    searchButton.addEventListener('click', function () {
        if (!isActive) {
            // Открыть окно поиска
            searchPopup.style.display = 'flex';
            isActive = true;
        }
        else {
            // Закрыть окно поиска
            searchPopup.style.display = 'none';
            isActive = false;
        }
    });
    // Закрытие окна при клике вне области окна поиска
    window.addEventListener('click', function (event) {
        if (event.target === searchPopup) {
            searchPopup.style.display = 'none';
            isActive = false;
            console.log('Закрытие при клике вне окна, isActive:', isActive);
        }
    });
}
else {
    console.error('Не найдены необходимые элементы для поиска!');
}
ymaps.ready(initMap);

console.log("dddddddd")

declare var ymaps: any; 

function initMap(): void {
    console.log("dddddddd")
    
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

    let lastValidPosition: number[] = [55.199440, 30.225416];

    function isMarkerInPolygon(): boolean {
        const position: number[] = marker.geometry.getCoordinates();
        return polygon.geometry.contains(position);
    }

    
    async function sendDataToServer(data: any): Promise<void> {
        try {
            const response = await fetch('http://127.0.0.1:8000/appeals/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data) 
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

    marker.events.add('drag', function () {
        
        const position: number[] = marker.geometry.getCoordinates();

        
        if (!isMarkerInPolygon()) {
            
            marker.geometry.setCoordinates(lastValidPosition);
        } else {
            
            lastValidPosition = position;
        }
    });

    const saveButton = document.getElementById('saveBtn');
    if (saveButton) {
        saveButton.addEventListener('click', function () {
            
            if (isMarkerInPolygon()) {
                const position = marker.geometry.getCoordinates();
               
                const formData = new FormData(document.getElementById('appealForm') as HTMLFormElement);
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
            } else {
                alert('Маркер находится вне полигона. Переместите его внутрь полигона перед сохранением.');
            }
        });
    }
}
const searchButton = document.getElementById('searchButton');
const searchPopup = document.getElementById('searchPopup');
let isActive: boolean = false;

// Проверка на существование элементов
if (searchButton && searchPopup) {
    searchButton.addEventListener('click', function () {
        if (!isActive) {
            // Открыть окно поиска
            searchPopup.style.display = 'flex';
            isActive = true;
        } else {
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
} else {
    console.error('Не найдены необходимые элементы для поиска!');
}

    
ymaps.ready(initMap);

declare var ymaps: any; 

function initMap(): void {
    
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
                    header: formData.get('header'),
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

ymaps.ready(initMap);

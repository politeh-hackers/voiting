declare var Inputmask: any;
declare var ymaps: any;

function initMap(): void {
    console.log("Map initialized");

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

    const saveButton = document.getElementById('saveBtn') as HTMLButtonElement;
    if (saveButton) {
        saveButton.addEventListener('click', function () {
            if (isMarkerInPolygon()) {
                console.log("Кнопка нажата");

                const position = marker.geometry.getCoordinates();
                const positionString = position.toString();

                const photosInput = document.getElementById('photos') as HTMLInputElement;
                const fileNames = photosInput.files 
                    ? Array.from(photosInput.files).map(file => file.name).join(', ') 
                    : ''; // Пустая строка, если файлов нет

                const categorySelect = document.getElementById('category') as HTMLSelectElement;
                const selectedCategoryText = categorySelect.options[categorySelect.selectedIndex].text;

                const lastName = (document.getElementById('lastName') as HTMLInputElement).value;
                const firstName = (document.getElementById('firstName') as HTMLInputElement).value;
                const patronymic = (document.getElementById('patronymic') as HTMLInputElement).value;
                const phone = (document.getElementById('phone') as HTMLInputElement).value;
                const text = (document.getElementById('text') as HTMLTextAreaElement).value;

                const appealData = {
                    location: positionString,
                    last_name: lastName,
                    first_name: firstName,
                    patronymic: patronymic,
                    phone: phone,
                    text: text,
                    photos: fileNames,
                    category: selectedCategoryText,
                };
                console.log('Отправляемые данные:', appealData);
                sendDataToServer(appealData);
                
            } else {
                alert('Маркер находится вне полигона. Переместите его внутрь полигона перед сохранением.');
            }
        });
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const burgerMenu = document.getElementById('burgerMenu') as HTMLElement;
    const headerCenter = document.querySelector('.header__center') as HTMLElement;

    if (burgerMenu) {
        burgerMenu.addEventListener('click', () => {
            headerCenter.classList.toggle('active'); // Переключаем класс active
        });
    }

    const modal = document.getElementById("appealForm") as HTMLElement;
    const closeModal = document.querySelector(".close-modal") as HTMLElement;
    const sendCodeBtn = document.getElementById("sendCodeBtn") as HTMLButtonElement;
    const confirmCodeBtn = document.getElementById("confirmCodeBtn") as HTMLButtonElement;
    const step1 = document.getElementById("step1") as HTMLElement;
    const step2 = document.getElementById("step2") as HTMLElement;
    const codeInputs = document.querySelectorAll(".code-box") as NodeListOf<HTMLInputElement>;

    // Маска для телефона
    const phoneInput = document.getElementById("phone") as HTMLInputElement;
    if (phoneInput) {
        new Inputmask("+375 (99) 999-99-99").mask(phoneInput);
    }

    // Открытие формы
    document.querySelector(".appeals__button")?.addEventListener("click", () => {
        if (modal) {
            modal.style.display = "flex";
        }
    });

    // Закрытие формы
    closeModal?.addEventListener("click", () => {
        if (modal) {
            modal.style.display = "none";
        }
    });

    // Отправка кода подтверждения
    sendCodeBtn?.addEventListener("click", () => {
        if (sendCodeBtn) {
            sendCodeBtn.disabled = true;
        }
        alert("Код отправлен! Введите его ниже.");
        if (confirmCodeBtn) {
            confirmCodeBtn.disabled = false;
        }
    });

    // Автоматический переход между полями кода
    codeInputs.forEach((input, index) => {
        input.addEventListener("input", (e) => {
            const target = e.target as HTMLInputElement;
            if (target.value && index < codeInputs.length - 1) {
                codeInputs[index + 1].focus();  // Переход к следующему полю
            }
        });
    });

    // Подтверждение кода
    confirmCodeBtn?.addEventListener("click", () => {
        alert("Телефон подтвержден!");
        if (step1 && step2) {
            step1.style.display = "none";
            step2.style.display = "block";
        }
    });
});

ymaps.ready(initMap);

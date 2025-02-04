declare var Inputmask: any;
declare var ymaps: any;

document.addEventListener("DOMContentLoaded", () => {
    const searchButton = document.getElementById("searchButton") as HTMLElement;
    const searchPopup = document.getElementById("searchPopup") as HTMLElement;
    const clearButton = document.getElementById("clearButton") as HTMLElement;
    
    if (searchButton && searchPopup) {
        searchButton.addEventListener("click", () => {
            searchPopup.style.display = searchPopup.style.display === "block" ? "none" : "block";
        });
    }

    if (clearButton) {
        clearButton.addEventListener("click", () => {
            (document.querySelector(".input__search") as HTMLInputElement).value = "";
        });
    }

    // Закрытие попапа при клике вне его
    document.addEventListener("click", (event) => {
        if (
            searchPopup.style.display === "block" &&
            !searchPopup.contains(event.target as Node) &&
            !searchButton.contains(event.target as Node)
        ) {
            searchPopup.style.display = "none";
        }
    });
});

function resetForm() {
    (document.getElementById('lastName') as HTMLInputElement).value = "";
    (document.getElementById('firstName') as HTMLInputElement).value = "";
    (document.getElementById('patronymic') as HTMLInputElement).value = "";
    (document.getElementById('phone') as HTMLInputElement).value = "";
    (document.getElementById('text') as HTMLTextAreaElement).value = "";
    (document.getElementById('category') as HTMLSelectElement).selectedIndex = 0;
    (document.getElementById('photos') as HTMLInputElement).value = "";
    document.querySelectorAll(".code-box").forEach(input => (input as HTMLInputElement).value = "");

    // Переключаемся обратно на первую часть формы
    const step1 = document.getElementById("step1") as HTMLElement;
    const step2 = document.getElementById("step2") as HTMLElement;
    step1.style.display = "flex";
    step2.style.display = "none";

    // Отключаем кнопку подтверждения кода
    (document.getElementById("confirmCodeBtn") as HTMLButtonElement).disabled = true;
}

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
    
    const modal = document.getElementById("appealForm") as HTMLElement;
    
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
                resetForm(); // Очистка формы после отправки
                modal.style.display = "none";
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
    const modal = document.getElementById("appealForm") as HTMLElement;
    const closeModal = document.querySelector(".close-modal") as HTMLElement;
    const sendCodeBtn = document.getElementById("sendCodeBtn") as HTMLButtonElement;
    const confirmCodeBtn = document.getElementById("confirmCodeBtn") as HTMLButtonElement;
    const codeInputs = document.querySelectorAll(".code-box") as NodeListOf<HTMLInputElement>;
    let countdownTimer: number | null = null;
    function startCountdown(duration: number) {
        let remainingTime = duration;
        sendCodeBtn.disabled = true;

        countdownTimer = setInterval(() => {
            if (remainingTime > 0) {
                sendCodeBtn.textContent = `Отправить повторно (${remainingTime})`;
                remainingTime--;
            } else {
                clearInterval(countdownTimer!);
                sendCodeBtn.textContent = "Отправить повторно";
                sendCodeBtn.disabled = false;
            }
        }, 1000);
    }
    // Маска для телефона
    const phoneInput = document.getElementById("phone") as HTMLInputElement;
    if (phoneInput) {
        new Inputmask("+375 (99) 999-99-99").mask(phoneInput);
    }

    // Открытие формы
    document.querySelector(".appeals__button")?.addEventListener("click", () => {
        modal.style.display = "flex";
        resetForm(); // Сбрасываем форму перед открытием
    });

    // Закрытие формы
    closeModal?.addEventListener("click", () => {
        const isConfirmed = confirm("Вы действительно хотите закрыть форму? Введённые данные будут утеряны.");
    
    if (isConfirmed) {
        modal.style.display = "none";
        resetForm();
    }
    });

    // Отправка кода подтверждения
    sendCodeBtn?.addEventListener("click", () => {
        alert("Код отправлен! Введите его ниже.");
        startCountdown(60); // Запуск таймера на 60 секунд
        confirmCodeBtn.disabled = false;
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
        document.getElementById("step1")!.style.display = "none";
        sendCodeBtn.disabled = false;
        document.getElementById("step2")!.style.display = "block";
    });
});

ymaps.ready(initMap);

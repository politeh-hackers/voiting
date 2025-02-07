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
    (document.getElementById('fileInput') as HTMLInputElement).value = "";
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
    [55.208408, 30.243153],
    [55.199440, 30.225416]
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
    
    async function sendDataToServer(data: FormData): Promise<void> {
        try {
            const response = await fetch('http://127.0.0.1:8000/appeals/', {
                method: 'POST',
                
                body: data, // FormData автоматически устанавливает корректные заголовки
            });
    
            if (response.ok) {
                console.log('Данные успешно отправлены');
                resetForm();
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
                const photosInput = document.getElementById('fileInput') as HTMLInputElement;
                const categorySelect = document.getElementById('category') as HTMLSelectElement;
                
                const formData = new FormData();
                formData.append("location", position.toString());
                formData.append("last_name", (document.getElementById('lastName') as HTMLInputElement).value);
                formData.append("first_name", (document.getElementById('firstName') as HTMLInputElement).value);
                formData.append("patronymic", (document.getElementById('patronymic') as HTMLInputElement).value);
                formData.append("phone", (document.getElementById('phone') as HTMLInputElement).value);
                formData.append("text", (document.getElementById('text') as HTMLTextAreaElement).value);
                formData.append("category", categorySelect.options[categorySelect.selectedIndex].text);
    
                // Добавляем файлы в FormData
                if (photosInput.files) {
                    Array.from(photosInput.files).forEach(file => {
                        formData.append("photos", file);
                    });
                }
    
                console.log('Отправляемые данные:', formData);
                sendDataToServer(formData);
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
    const confirmBtn = document.getElementById("confirmBtn") as HTMLButtonElement;
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
        
        confirmBtn.disabled = false;
    });
    confirmBtn?.addEventListener("click", () => {
        alert("Телефон подтвержден!");
        document.getElementById("step1")!.style.display = "none";
        sendCodeBtn.disabled = false;

        document.getElementById("step2")!.style.display = "block";
    });
});
const fileInput = document.getElementById("fileInput") as HTMLInputElement;
const uploadButton = document.getElementById("uploadButton") as HTMLButtonElement;
const previewContainer = document.getElementById("previewContainer") as HTMLDivElement;
const previewImage = document.getElementById("previewImage") as HTMLImageElement;
const deleteButton = document.getElementById("deleteButton") as HTMLButtonElement;

let selectedFile: File | null = null;
let uploadedFileUrl: string | null = null;  // Переменная для хранения URL загруженного файла

// Обработчик выбора файла
fileInput.addEventListener("change", (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (target.files && target.files[0]) {
        selectedFile = target.files[0];
        const reader = new FileReader();

        reader.onload = (e) => {
            previewImage.src = e.target?.result as string;
            previewContainer.classList.remove("hidden");
        };

        reader.readAsDataURL(selectedFile);
        uploadButton.disabled = false;
    }
});

// Обработчик загрузки файла
uploadButton.addEventListener("click", async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append("image", selectedFile);

    try {
        const response = await fetch("http://localhost:8000/admin/image", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error("Ошибка загрузки");

        const data = await response.json();
        console.log(data)  // Получаем ответ от сервера (например, URL файла)
        uploadedFileUrl = data.url;  // Предполагаем, что сервер возвращает URL загруженного файла
        console.log(uploadedFileUrl)
        alert("Файл загружен успешно!");
        uploadButton.disabled = true;
    } catch (error) {
        alert(error);
    }
});

// Обработчик удаления файла с сервера
deleteButton.addEventListener("click", async () => {
    console.log(uploadedFileUrl)
    if (uploadedFileUrl) {
        try {
            const response = await fetch(uploadedFileUrl, {
                method: "DELETE",
                headers: {
                     "Content-Type": "application/json",
                     "Accept": "application/json"
                }
            });

            if (response.ok) {
                alert("Файл удалён успешно!");
                // Скрываем превью и очищаем форму
                previewContainer.classList.add("hidden");
                previewImage.src = "";
                fileInput.value = "";
                uploadButton.disabled = true;
                selectedFile = null;
                uploadedFileUrl = null;  // Очищаем URL
            } else {
                throw new Error("Ошибка при удалении файла");
            }
        } catch (error) {
            alert(error);
        }
    } else {
        // Если файл не был загружен, просто очищаем форму
        previewContainer.classList.add("hidden");
        previewImage.src = "";
        fileInput.value = "";
        uploadButton.disabled = true;
        selectedFile = null;
    }
});


ymaps.ready(initMap);

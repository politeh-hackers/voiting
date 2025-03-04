declare var ymaps: any;
function validateStep1() {
    let isValid = true;

    const lastName = document.getElementById('lastName') as HTMLInputElement;
    const firstName = document.getElementById('firstName') as HTMLInputElement;
    const patronymic = document.getElementById('patronymic') as HTMLInputElement;
    const phone = document.getElementById('phone') as HTMLInputElement;

    document.querySelectorAll('.error-message').forEach((el) => el.textContent = '');
    document.querySelectorAll('input').forEach((input) => input.style.border = '');

    if (lastName.value.trim() === '') {
        document.getElementById('lastNameError')!.textContent = 'Это поле обязательно для заполнения';
        lastName.style.border = '1px solid red';
        isValid = false;
    }

    if (firstName.value.trim() === '') {
        document.getElementById('firstNameError')!.textContent = 'Это поле обязательно для заполнения';
        firstName.style.border = '1px solid red';
        isValid = false;
    }

    if (patronymic.value.trim() === '') {
        document.getElementById('patronymicError')!.textContent = 'Это поле обязательно для заполнения';
        patronymic.style.border = '1px solid red';
        isValid = false;
    }

    if (phone.value.trim() === '') {
        document.getElementById('phoneError')!.textContent = 'Это поле обязательно для заполнения';
        phone.style.border = '1px solid red';
        isValid = false;
    }

    return isValid;
}

function validateStep2() {
    let isValid = true;

    const category = document.getElementById('category') as HTMLSelectElement;
    if (category.value === '') {
        document.getElementById('categoryError')!.textContent = 'Выберите категорию';
        category.style.border = '1px solid red';
        isValid = false;
    }

    const text = document.getElementById('text') as HTMLTextAreaElement;
    if (text.value.trim().length < 500 || text.value.trim().length > 2000) {
        document.getElementById('textError')!.textContent = 'Текст должен быть от 500 до 2000 символов';
        text.style.border = '1px solid red';
        isValid = false;
    }

    return isValid;
}



document.addEventListener("DOMContentLoaded", () => {
    const searchButton = document.getElementById("searchButton") as HTMLElement;
    const searchPopup = document.getElementById("searchPopup") as HTMLElement;
    const clearButton = document.getElementById("clearButton") as HTMLElement;
    
    if (searchButton && searchPopup) {
        searchButton.addEventListener("click", () => {
            searchPopup.style.display = searchPopup.style.display === "flex" ? "none" : "flex";
        });
    }

    if (clearButton) {
        clearButton.addEventListener("click", () => {
            (document.querySelector(".input__search") as HTMLInputElement).value = "";
        });
    }

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

    allFiles = [];

    const previewContainer = document.getElementById("previewContainer") as HTMLDivElement;
    
    const images = previewContainer.querySelectorAll("img");
    images.forEach(img => img.remove());
    const step1 = document.getElementById("step1") as HTMLElement;
    const step2 = document.getElementById("step2") as HTMLElement;
    step1.style.display = "flex";
    step2.style.display = "none";

    const confirmCodeBtn = document.getElementById("confirmCodeBtn") as HTMLButtonElement;
    confirmCodeBtn.disabled = true;
}

function initMap(): void {
    console.log("Map initialized");

    const map = new ymaps.Map('map', {
        center: [55.200000, 30.250000],
        zoom: 14,
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
            const response = await fetch('http://127.0.0.1:8000/appeals/appeals', {
                method: 'POST',
                
                body: data, 
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
                if(validateStep2()){
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
    
                allFiles.forEach(file => {
                    formData.append("photos", file); 
                });
    
                console.log('Отправляемые данные:', formData);
                sendDataToServer(formData);
            } else {
                alert('Маркер находится вне полигона. Переместите его внутрь полигона перед сохранением.');
            }
        }
        });
    }
    
}
document.addEventListener("DOMContentLoaded", () => {
    const burgerMenu = document.getElementById("burgerMenu") as HTMLElement | null;
    const menu = document.querySelector(".header__center") as HTMLElement | null;

    if (burgerMenu && menu) {
        burgerMenu.addEventListener("click", () => {
            menu.classList.toggle("active");
        });

        // Закрытие меню при клике вне его области
        document.addEventListener("click", (event: MouseEvent) => {
            const target = event.target as Node;
            if (!menu.contains(target) && !burgerMenu.contains(target)) {
                menu.classList.remove("active");
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const phoneInput = document.getElementById("phone") as HTMLInputElement;

    if (phoneInput) {
        phoneInput.addEventListener("input", formatPhoneInput);
        phoneInput.addEventListener("keydown", handlePhoneBackspace);
    }

    function formatPhoneInput(event: Event) {
        const input = event.target as HTMLInputElement;
        let value = input.value.replace(/\D/g, ""); 

        if (value.startsWith("375")) {
            value = value.slice(3); 
        }

        if (value.length > 9) {
            value = value.slice(0, 9); 
        }

        let formattedValue = "+375 ";
        if (value.length > 0) {
            formattedValue += "(" + value.slice(0, 2);
        }
        if (value.length > 2) {
            formattedValue += ") " + value.slice(2, 5);
        }
        if (value.length > 5) {
            formattedValue += "-" + value.slice(5, 7);
        }
        if (value.length > 7) {
            formattedValue += "-" + value.slice(7, 9);
        }

        input.value = formattedValue;
    }

    function handlePhoneBackspace(event: KeyboardEvent) {
        const input = event.target as HTMLInputElement;
        if (event.key === "Backspace" && input.value.length <= 7) {
            event.preventDefault();
            input.value = "+375 "; 
        }
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("appealForm") as HTMLElement;
    const mobileClose = document.querySelector(".mobile-close") as HTMLElement;
    const desktopClose = document.querySelector(".desktop-close") as HTMLElement;
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

    document.querySelector(".appeals__button")?.addEventListener("click", () => {
        modal.style.display = "flex";
        resetForm();
    });

    // Обработчик для мобильной версии
    mobileClose?.addEventListener("click", () => {
        const isConfirmed = confirm("Вы действительно хотите закрыть форму? Введённые данные будут утеряны.");
        if (isConfirmed) {
            modal.classList.add('closing');
            setTimeout(() => {
                modal.style.display = "none";
                modal.classList.remove('closing');
                resetForm();
            }, 500);
        }
    });

    // Обработчик для десктопной версии
    desktopClose?.addEventListener("click", () => {
        const isConfirmed = confirm("Вы действительно хотите закрыть форму? Введённые данные будут утеряны.");
        if (isConfirmed) {
            modal.classList.add('closing');
            setTimeout(() => {
                modal.style.display = "none";
                modal.classList.remove('closing');
                resetForm();
            }, 500);
        }
    });

    // Закрытие формы при клике вне её области
    window.addEventListener("click", (event: MouseEvent) => {
        if (event.target === modal) {
            const isConfirmed = confirm("Вы действительно хотите закрыть форму? Введённые данные будут утеряны.");
            if (isConfirmed) {
                modal.classList.add('closing');
                setTimeout(() => {
                    modal.style.display = "none";
                    modal.classList.remove('closing');
                    resetForm();
                }, 500);
            }
        }
    });

    sendCodeBtn?.addEventListener("click", () => {
        alert("Код отправлен! Введите его ниже.");
        startCountdown(60);
        confirmCodeBtn.disabled = false;
    });

    codeInputs.forEach((input, index) => {
        input.addEventListener("input", (e) => {
            const target = e.target as HTMLInputElement;
            if (target.value && index < codeInputs.length - 1) {
                codeInputs[index + 1].focus(); 
            }
        });
    });

    // Подтверждение кода
    confirmCodeBtn?.addEventListener("click", () => {
        alert("Телефон подтвержден!");
        
        confirmBtn.disabled = false;
    });
    confirmBtn?.addEventListener("click", () => {
        if (validateStep1()) {
        alert("Телефон подтвержден!");
        document.getElementById("step1")!.style.display = "none";
        sendCodeBtn.disabled = false;
        const step2 = document.getElementById("step2") as HTMLElement;
        step2.style.removeProperty("display");
        step2.classList.add("step2");
        }
        else{
            throw new Error("dsdsd");;
            
        }
    });
});
let allFiles: File[] = [];

const fileInput = document.getElementById("fileInput") as HTMLInputElement;
const previewContainer = document.getElementById("previewContainer") as HTMLDivElement;

fileInput.addEventListener("change", (event: Event) => {
    const target = event.target as HTMLInputElement;
    if (!target.files) return;

    Array.from(target.files).forEach((file) => {
        allFiles.push(file);

        const reader = new FileReader();
        reader.onload = (e) => {
            const img = document.createElement("img");
            img.src = e.target?.result as string;
            img.classList.add("images_preview");

            previewContainer.insertBefore(img, previewContainer.lastElementChild);
        };

        reader.readAsDataURL(file);
    });
});
// Обработчик удаления файла с сервера
// deleteButton.addEventListener("click", async () => {
//     console.log(uploadedFileUrl)
//     if (uploadedFileUrl) {
//         try {
//             const response = await fetch(uploadedFileUrl, {
//                 method: "DELETE",
//                 headers: {
//                      "Content-Type": "application/json",
//                      "Accept": "application/json"
//                 }
//             });

//             if (response.ok) {
//                 alert("Файл удалён успешно!");
//                 // Скрываем превью и очищаем форму
//                 previewContainer.classList.add("hidden");
//                 previewImage.src = "";
//                 fileInput.value = "";
//                 uploadButton.disabled = true;
//                 selectedFile = null;
//                 uploadedFileUrl = null;  // Очищаем URL
//             } else {
//                 throw new Error("Ошибка при удалении файла");
//             }
//         } catch (error) {
//             alert(error);
//         }
//     } else {
//         // Если файл не был загружен, просто очищаем форму
//         previewContainer.classList.add("hidden");
//         previewImage.src = "";
//         fileInput.value = "";
//         uploadButton.disabled = true;
//         selectedFile = null;
//     }
// });


ymaps.ready(initMap);

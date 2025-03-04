var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g = Object.create((typeof Iterator === "function" ? Iterator : Object).prototype);
    return g.next = verb(0), g["throw"] = verb(1), g["return"] = verb(2), typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
function validateStep1() {
    var isValid = true;
    var lastName = document.getElementById('lastName');
    var firstName = document.getElementById('firstName');
    var patronymic = document.getElementById('patronymic');
    var phone = document.getElementById('phone');
    document.querySelectorAll('.error-message').forEach(function (el) { return el.textContent = ''; });
    document.querySelectorAll('input').forEach(function (input) { return input.style.border = ''; });
    if (lastName.value.trim() === '') {
        document.getElementById('lastNameError').textContent = 'Это поле обязательно для заполнения';
        lastName.style.border = '1px solid red';
        isValid = false;
    }
    if (firstName.value.trim() === '') {
        document.getElementById('firstNameError').textContent = 'Это поле обязательно для заполнения';
        firstName.style.border = '1px solid red';
        isValid = false;
    }
    if (patronymic.value.trim() === '') {
        document.getElementById('patronymicError').textContent = 'Это поле обязательно для заполнения';
        patronymic.style.border = '1px solid red';
        isValid = false;
    }
    if (phone.value.trim() === '') {
        document.getElementById('phoneError').textContent = 'Это поле обязательно для заполнения';
        phone.style.border = '1px solid red';
        isValid = false;
    }
    return isValid;
}
function validateStep2() {
    var isValid = true;
    var category = document.getElementById('category');
    if (category.value === '') {
        document.getElementById('categoryError').textContent = 'Выберите категорию';
        category.style.border = '1px solid red';
        isValid = false;
    }
    var text = document.getElementById('text');
    if (text.value.trim().length < 500 || text.value.trim().length > 2000) {
        document.getElementById('textError').textContent = 'Текст должен быть от 500 до 2000 символов';
        text.style.border = '1px solid red';
        isValid = false;
    }
    return isValid;
}
document.addEventListener("DOMContentLoaded", function () {
    var searchButton = document.getElementById("searchButton");
    var searchPopup = document.getElementById("searchPopup");
    var clearButton = document.getElementById("clearButton");
    if (searchButton && searchPopup) {
        searchButton.addEventListener("click", function () {
            searchPopup.style.display = searchPopup.style.display === "flex" ? "none" : "flex";
        });
    }
    if (clearButton) {
        clearButton.addEventListener("click", function () {
            document.querySelector(".input__search").value = "";
        });
    }
    document.addEventListener("click", function (event) {
        if (searchPopup.style.display === "block" &&
            !searchPopup.contains(event.target) &&
            !searchButton.contains(event.target)) {
            searchPopup.style.display = "none";
        }
    });
});
function resetForm() {
    document.getElementById('lastName').value = "";
    document.getElementById('firstName').value = "";
    document.getElementById('patronymic').value = "";
    document.getElementById('phone').value = "";
    document.getElementById('text').value = "";
    document.getElementById('category').selectedIndex = 0;
    document.getElementById('fileInput').value = "";
    document.querySelectorAll(".code-box").forEach(function (input) { return input.value = ""; });
    allFiles = [];
    var previewContainer = document.getElementById("previewContainer");
    var images = previewContainer.querySelectorAll("img");
    images.forEach(function (img) { return img.remove(); });
    var step1 = document.getElementById("step1");
    var step2 = document.getElementById("step2");
    step1.style.display = "flex";
    step2.style.display = "none";
    var confirmCodeBtn = document.getElementById("confirmCodeBtn");
    confirmCodeBtn.disabled = true;
}
function initMap() {
    console.log("Map initialized");
    var map = new ymaps.Map('map', {
        center: [55.200000, 30.250000],
        zoom: 14,
    });
    var coordinates = [
        [55.199440, 30.225416],
        [55.194158, 30.229461],
        [55.197758, 30.266929],
        [55.208433, 30.271005],
        [55.208408, 30.243153],
        [55.199440, 30.225416]
    ];
    var polygon = new ymaps.Polygon([coordinates], {}, {
        fillColor: '#6699FF33',
        strokeColor: '#0000FF',
        strokeWidth: 2
    });
    map.geoObjects.add(polygon);
    var marker = new ymaps.Placemark([55.199440, 30.225416], {
        hintContent: 'Перетащи меня!'
    });
    map.geoObjects.add(marker);
    marker.options.set('draggable', true);
    var lastValidPosition = [55.199440, 30.225416];
    function isMarkerInPolygon() {
        var position = marker.geometry.getCoordinates();
        return polygon.geometry.contains(position);
    }
    var modal = document.getElementById("appealForm");
    function sendDataToServer(data) {
        return __awaiter(this, void 0, void 0, function () {
            var response, error_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, fetch('http://127.0.0.1:8000/appeals/appeals', {
                                method: 'POST',
                                body: data,
                            })];
                    case 1:
                        response = _a.sent();
                        if (response.ok) {
                            console.log('Данные успешно отправлены');
                            resetForm();
                            modal.style.display = "none";
                        }
                        else {
                            console.error('Ошибка при отправке данных');
                        }
                        return [3 /*break*/, 3];
                    case 2:
                        error_1 = _a.sent();
                        console.error('Ошибка сети:', error_1);
                        return [3 /*break*/, 3];
                    case 3: return [2 /*return*/];
                }
            });
        });
    }
    marker.events.add('drag', function () {
        var position = marker.geometry.getCoordinates();
        if (!isMarkerInPolygon()) {
            marker.geometry.setCoordinates(lastValidPosition);
        }
        else {
            lastValidPosition = position;
        }
    });
    var saveButton = document.getElementById('saveBtn');
    if (saveButton) {
        saveButton.addEventListener('click', function () {
            if (isMarkerInPolygon()) {
                if (validateStep2()) {
                    console.log("Кнопка нажата");
                    var position = marker.geometry.getCoordinates();
                    var photosInput = document.getElementById('fileInput');
                    var categorySelect = document.getElementById('category');
                    var formData_1 = new FormData();
                    formData_1.append("location", position.toString());
                    formData_1.append("last_name", document.getElementById('lastName').value);
                    formData_1.append("first_name", document.getElementById('firstName').value);
                    formData_1.append("patronymic", document.getElementById('patronymic').value);
                    formData_1.append("phone", document.getElementById('phone').value);
                    formData_1.append("text", document.getElementById('text').value);
                    formData_1.append("category", categorySelect.options[categorySelect.selectedIndex].text);
                    allFiles.forEach(function (file) {
                        formData_1.append("photos", file);
                    });
                    console.log('Отправляемые данные:', formData_1);
                    sendDataToServer(formData_1);
                }
                else {
                    alert('Маркер находится вне полигона. Переместите его внутрь полигона перед сохранением.');
                }
            }
        });
    }
}
document.addEventListener("DOMContentLoaded", function () {
    var burgerMenu = document.getElementById("burgerMenu");
    var menu = document.querySelector(".header__center");
    if (burgerMenu && menu) {
        burgerMenu.addEventListener("click", function () {
            menu.classList.toggle("active");
        });
        // Закрытие меню при клике вне его области
        document.addEventListener("click", function (event) {
            var target = event.target;
            if (!menu.contains(target) && !burgerMenu.contains(target)) {
                menu.classList.remove("active");
            }
        });
    }
});
document.addEventListener("DOMContentLoaded", function () {
    var phoneInput = document.getElementById("phone");
    if (phoneInput) {
        phoneInput.addEventListener("input", formatPhoneInput);
        phoneInput.addEventListener("keydown", handlePhoneBackspace);
    }
    function formatPhoneInput(event) {
        var input = event.target;
        var value = input.value.replace(/\D/g, "");
        if (value.startsWith("375")) {
            value = value.slice(3);
        }
        if (value.length > 9) {
            value = value.slice(0, 9);
        }
        var formattedValue = "+375 ";
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
    function handlePhoneBackspace(event) {
        var input = event.target;
        if (event.key === "Backspace" && input.value.length <= 7) {
            event.preventDefault();
            input.value = "+375 ";
        }
    }
});
document.addEventListener("DOMContentLoaded", function () {
    var _a;
    var modal = document.getElementById("appealForm");
    var mobileClose = document.querySelector(".mobile-close");
    var desktopClose = document.querySelector(".desktop-close");
    var sendCodeBtn = document.getElementById("sendCodeBtn");
    var confirmCodeBtn = document.getElementById("confirmCodeBtn");
    var confirmBtn = document.getElementById("confirmBtn");
    var codeInputs = document.querySelectorAll(".code-box");
    var countdownTimer = null;
    function startCountdown(duration) {
        var remainingTime = duration;
        sendCodeBtn.disabled = true;
        countdownTimer = setInterval(function () {
            if (remainingTime > 0) {
                sendCodeBtn.textContent = "\u041E\u0442\u043F\u0440\u0430\u0432\u0438\u0442\u044C \u043F\u043E\u0432\u0442\u043E\u0440\u043D\u043E (".concat(remainingTime, ")");
                remainingTime--;
            }
            else {
                clearInterval(countdownTimer);
                sendCodeBtn.textContent = "Отправить повторно";
                sendCodeBtn.disabled = false;
            }
        }, 1000);
    }
    (_a = document.querySelector(".appeals__button")) === null || _a === void 0 ? void 0 : _a.addEventListener("click", function () {
        modal.style.display = "flex";
        resetForm();
    });
    // Обработчик для мобильной версии
    mobileClose === null || mobileClose === void 0 ? void 0 : mobileClose.addEventListener("click", function () {
        var isConfirmed = confirm("Вы действительно хотите закрыть форму? Введённые данные будут утеряны.");
        if (isConfirmed) {
            modal.classList.add('closing');
            setTimeout(function () {
                modal.style.display = "none";
                modal.classList.remove('closing');
                resetForm();
            }, 500);
        }
    });
    // Обработчик для десктопной версии
    desktopClose === null || desktopClose === void 0 ? void 0 : desktopClose.addEventListener("click", function () {
        var isConfirmed = confirm("Вы действительно хотите закрыть форму? Введённые данные будут утеряны.");
        if (isConfirmed) {
            modal.classList.add('closing');
            setTimeout(function () {
                modal.style.display = "none";
                modal.classList.remove('closing');
                resetForm();
            }, 500);
        }
    });
    // Закрытие формы при клике вне её области
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            var isConfirmed = confirm("Вы действительно хотите закрыть форму? Введённые данные будут утеряны.");
            if (isConfirmed) {
                modal.classList.add('closing');
                setTimeout(function () {
                    modal.style.display = "none";
                    modal.classList.remove('closing');
                    resetForm();
                }, 500);
            }
        }
    });
    sendCodeBtn === null || sendCodeBtn === void 0 ? void 0 : sendCodeBtn.addEventListener("click", function () {
        alert("Код отправлен! Введите его ниже.");
        startCountdown(60);
        confirmCodeBtn.disabled = false;
    });
    codeInputs.forEach(function (input, index) {
        input.addEventListener("input", function (e) {
            var target = e.target;
            if (target.value && index < codeInputs.length - 1) {
                codeInputs[index + 1].focus();
            }
        });
    });
    // Подтверждение кода
    confirmCodeBtn === null || confirmCodeBtn === void 0 ? void 0 : confirmCodeBtn.addEventListener("click", function () {
        alert("Телефон подтвержден!");
        confirmBtn.disabled = false;
    });
    confirmBtn === null || confirmBtn === void 0 ? void 0 : confirmBtn.addEventListener("click", function () {
        if (validateStep1()) {
            alert("Телефон подтвержден!");
            document.getElementById("step1").style.display = "none";
            sendCodeBtn.disabled = false;
            var step2 = document.getElementById("step2");
            step2.style.removeProperty("display");
            step2.classList.add("step2");
        }
        else {
            throw new Error("dsdsd");
            ;
        }
    });
});
var allFiles = [];
var fileInput = document.getElementById("fileInput");
var previewContainer = document.getElementById("previewContainer");
fileInput.addEventListener("change", function (event) {
    var target = event.target;
    if (!target.files)
        return;
    Array.from(target.files).forEach(function (file) {
        allFiles.push(file);
        var reader = new FileReader();
        reader.onload = function (e) {
            var _a;
            var img = document.createElement("img");
            img.src = (_a = e.target) === null || _a === void 0 ? void 0 : _a.result;
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

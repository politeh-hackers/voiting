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
function initMap() {
    console.log("Map initialized");
    var map = new ymaps.Map('map', {
        center: [55.200000, 30.250000],
        zoom: 10,
    });
    var coordinates = [
        [55.199440, 30.225416],
        [55.194158, 30.229461],
        [55.197758, 30.266929],
        [55.208433, 30.271005],
        [55.208408, 30.243153]
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
    function sendDataToServer(data) {
        return __awaiter(this, void 0, void 0, function () {
            var response, error_1;
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        _a.trys.push([0, 2, , 3]);
                        return [4 /*yield*/, fetch('http://127.0.0.1:8000/appeals/', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json'
                                },
                                body: JSON.stringify(data)
                            })];
                    case 1:
                        response = _a.sent();
                        if (response.ok) {
                            console.log('Данные успешно отправлены');
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
                console.log("Кнопка нажата");
                var position = marker.geometry.getCoordinates();
                var positionString = position.toString();
                var photosInput = document.getElementById('photos');
                var fileNames = photosInput.files
                    ? Array.from(photosInput.files).map(function (file) { return file.name; }).join(', ')
                    : ''; // Пустая строка, если файлов нет
                var categorySelect = document.getElementById('category');
                var selectedCategoryText = categorySelect.options[categorySelect.selectedIndex].text;
                var lastName = document.getElementById('lastName').value;
                var firstName = document.getElementById('firstName').value;
                var patronymic = document.getElementById('patronymic').value;
                var phone = document.getElementById('phone').value;
                var text = document.getElementById('text').value;
                var appealData = {
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
            }
            else {
                alert('Маркер находится вне полигона. Переместите его внутрь полигона перед сохранением.');
            }
        });
    }
}
document.addEventListener("DOMContentLoaded", function () {
    var _a;
    var burgerMenu = document.getElementById('burgerMenu');
    var headerCenter = document.querySelector('.header__center');
    if (burgerMenu) {
        burgerMenu.addEventListener('click', function () {
            headerCenter.classList.toggle('active'); // Переключаем класс active
        });
    }
    var modal = document.getElementById("appealForm");
    var closeModal = document.querySelector(".close-modal");
    var sendCodeBtn = document.getElementById("sendCodeBtn");
    var confirmCodeBtn = document.getElementById("confirmCodeBtn");
    var step1 = document.getElementById("step1");
    var step2 = document.getElementById("step2");
    var codeInputs = document.querySelectorAll(".code-box");
    // Маска для телефона
    var phoneInput = document.getElementById("phone");
    if (phoneInput) {
        new Inputmask("+375 (99) 999-99-99").mask(phoneInput);
    }
    // Открытие формы
    (_a = document.querySelector(".appeals__button")) === null || _a === void 0 ? void 0 : _a.addEventListener("click", function () {
        if (modal) {
            modal.style.display = "flex";
        }
    });
    // Закрытие формы
    closeModal === null || closeModal === void 0 ? void 0 : closeModal.addEventListener("click", function () {
        if (modal) {
            modal.style.display = "none";
        }
    });
    // Отправка кода подтверждения
    sendCodeBtn === null || sendCodeBtn === void 0 ? void 0 : sendCodeBtn.addEventListener("click", function () {
        if (sendCodeBtn) {
            sendCodeBtn.disabled = true;
        }
        alert("Код отправлен! Введите его ниже.");
        if (confirmCodeBtn) {
            confirmCodeBtn.disabled = false;
        }
    });
    // Автоматический переход между полями кода
    codeInputs.forEach(function (input, index) {
        input.addEventListener("input", function (e) {
            var target = e.target;
            if (target.value && index < codeInputs.length - 1) {
                codeInputs[index + 1].focus(); // Переход к следующему полю
            }
        });
    });
    // Подтверждение кода
    confirmCodeBtn === null || confirmCodeBtn === void 0 ? void 0 : confirmCodeBtn.addEventListener("click", function () {
        alert("Телефон подтвержден!");
        if (step1 && step2) {
            step1.style.display = "none";
            step2.style.display = "block";
        }
    });
});
ymaps.ready(initMap);

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".appeals_photos-container").forEach(function (container) {
        var photoContainer = container.querySelector(".appeals_photos");
        var leftBtn = container.querySelector(".left-btn");
        var rightBtn = container.querySelector(".right-btn");
        if (!photoContainer || !leftBtn || !rightBtn)
            return;
        var photos = photoContainer.querySelectorAll(".appeal_photo");
        // Если фото 2 или меньше, скрываем кнопки и градиент
        if (photos.length <= 2) {
            leftBtn.style.display = "none";
            rightBtn.style.display = "none";
            photoContainer.style.maskImage = "none";
            return;
        }
        // Включаем градиент справа
        photoContainer.style.maskImage = "linear-gradient(to right, rgba(0, 0, 0, 1) 80%, rgba(0, 0, 0, 0))";
        photoContainer.style.transition = "mask-image 0.3s ease"; // Плавный переход для изменения градиента
        var scrollAmount = 100; // Количество пикселей для прокрутки
        // Обработчик клика на левую кнопку
        leftBtn.addEventListener("click", function () {
            photoContainer.scrollBy({ left: -scrollAmount, behavior: "smooth" });
        });
        // Обработчик клика на правую кнопку
        rightBtn.addEventListener("click", function () {
            photoContainer.scrollBy({ left: scrollAmount, behavior: "smooth" });
        });
        // Функция для проверки состояния кнопок и динамического изменения маски
        var updateButtonsVisibility = function () {
            var scrollLeft = photoContainer.scrollLeft;
            var scrollWidth = photoContainer.scrollWidth;
            var clientWidth = photoContainer.clientWidth;
            // Показываем/скрываем левую кнопку в зависимости от прокрутки
            if (scrollLeft > 0) {
                leftBtn.style.display = "block";
            }
            else {
                leftBtn.style.display = "none";
            }
            // Показываем/скрываем правую кнопку в зависимости от прокрутки
            if (scrollLeft + clientWidth < scrollWidth - 1) {
                rightBtn.style.display = "block"; // Если есть пространство для прокрутки вправо
            }
            else {
                rightBtn.style.display = "none"; // Если достигнут конец
            }
            // Добавляем градиенты с обеих сторон, если прокручиваем, но не достигли конца
            if (scrollLeft > 0 && scrollLeft + clientWidth < scrollWidth) {
                photoContainer.style.maskImage = "linear-gradient(to left, transparent, rgba(0, 0, 0, 1) 80%, transparent), linear-gradient(to right, transparent, rgba(0, 0, 0, 1) 80%, transparent)"; // Градиенты с обеих сторон
            }
            else if (scrollLeft > 0) {
                photoContainer.style.maskImage = "linear-gradient(to left, rgba(0, 0, 0, 1) 80%, rgba(0, 0, 0, 0))"; // Градиент слева
            }
            else if (scrollLeft + clientWidth < scrollWidth - 10) {
                photoContainer.style.maskImage = "linear-gradient(to right, rgba(0, 0, 0, 1) 80%, rgba(0, 0, 0, 0))"; // Градиент справа
            }
            else {
                photoContainer.style.maskImage = "none"; // Убираем градиенты, если в конце
            }
        };
        // Вызываем при загрузке страницы, чтобы установить правильное состояние кнопок
        updateButtonsVisibility();
        // Добавляем слушатель события для обновления состояния кнопок при прокрутке
        photoContainer.addEventListener("scroll", updateButtonsVisibility);
    });
    document.querySelectorAll(".cards").forEach(function (container) {
        var mapToggleBtn = document.getElementById('map-toggle-btn');
        var mapContainer = document.querySelector('.map__container');
        var chevronIcon = document.getElementById('chevron-icon');
        // Проверяем, существует ли контейнер карты
        if (!mapContainer || !chevronIcon)
            return;
        // Добавляем обработчик события для кнопки
        mapToggleBtn.addEventListener('click', function () {
            // Переключаем класс 'open' у контейнера карты
            mapContainer.classList.toggle('open');
            // Переключаем класс 'rotate' у иконки
            chevronIcon.classList.toggle('rotate');
        });
    });
});

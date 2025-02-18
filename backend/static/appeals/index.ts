document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".appeals_photos-container").forEach((container) => {
        const photoContainer = container.querySelector(".appeals_photos") as HTMLElement | null;
        const leftBtn = container.querySelector(".left-btn") as HTMLButtonElement | null;
        const rightBtn = container.querySelector(".right-btn") as HTMLButtonElement | null;

        if (!photoContainer || !leftBtn || !rightBtn) return;

        const photos = photoContainer.querySelectorAll(".appeal_photo");

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

        const scrollAmount: number = 100; // Количество пикселей для прокрутки

        // Обработчик клика на левую кнопку
        leftBtn.addEventListener("click", () => {
            photoContainer.scrollBy({ left: -scrollAmount, behavior: "smooth" });
        });

        // Обработчик клика на правую кнопку
        rightBtn.addEventListener("click", () => {
            photoContainer.scrollBy({ left: scrollAmount, behavior: "smooth" });
        });

        // Функция для проверки состояния кнопок и динамического изменения маски
        const updateButtonsVisibility = (): void => {
            const scrollLeft = photoContainer.scrollLeft;
            const scrollWidth = photoContainer.scrollWidth;
            const clientWidth = photoContainer.clientWidth;

            // Показываем/скрываем левую кнопку в зависимости от прокрутки
            if (scrollLeft > 0) {
                leftBtn.style.display = "block";
            } else {
                leftBtn.style.display = "none";
            }

            // Показываем/скрываем правую кнопку в зависимости от прокрутки
            if (scrollLeft + clientWidth < scrollWidth - 1) {
                rightBtn.style.display = "block"; // Если есть пространство для прокрутки вправо
            } else {
                rightBtn.style.display = "none"; // Если достигнут конец
                
            }

            // Добавляем градиенты с обеих сторон, если прокручиваем, но не достигли конца
            if (scrollLeft > 0 && scrollLeft + clientWidth < scrollWidth) {
                photoContainer.style.maskImage = "linear-gradient(to left, transparent, rgba(0, 0, 0, 1) 80%, transparent), linear-gradient(to right, transparent, rgba(0, 0, 0, 1) 80%, transparent)"; // Градиенты с обеих сторон
            } else if (scrollLeft > 0) {
                photoContainer.style.maskImage = "linear-gradient(to left, rgba(0, 0, 0, 1) 80%, rgba(0, 0, 0, 0))"; // Градиент слева
            } else if (scrollLeft + clientWidth < scrollWidth - 10) {
                photoContainer.style.maskImage = "linear-gradient(to right, rgba(0, 0, 0, 1) 80%, rgba(0, 0, 0, 0))"; // Градиент справа
            } else {
                photoContainer.style.maskImage = "none"; // Убираем градиенты, если в конце
            }
        };

        // Вызываем при загрузке страницы, чтобы установить правильное состояние кнопок
        updateButtonsVisibility();

        // Добавляем слушатель события для обновления состояния кнопок при прокрутке
        photoContainer.addEventListener("scroll", updateButtonsVisibility);
    });
});

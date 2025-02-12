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

        // Включаем градиент
        photoContainer.style.maskImage = "linear-gradient(to right, rgba(0, 0, 0, 1) 80%, rgba(0, 0, 0, 0))";

        const scrollAmount: number = 150; // Количество пикселей для прокрутки

        leftBtn.addEventListener("click", () => {
            photoContainer.scrollBy({ left: -scrollAmount, behavior: "smooth" });
        });

        rightBtn.addEventListener("click", () => {
            photoContainer.scrollBy({ left: scrollAmount, behavior: "smooth" });
        });
    });
});

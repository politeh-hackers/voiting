document.addEventListener("DOMContentLoaded", () => {
    const loadMoreButton = document.getElementById("load-more-button") as HTMLButtonElement;
    const gradientContainer = document.querySelector(".gradient-container") as HTMLElement;
    const appealCards = document.querySelectorAll(".card__appeal") as NodeListOf<HTMLElement>;

    const INITIAL_VISIBLE_CARDS = 8;

    // Скрываем все карточки после 8-й
    appealCards.forEach((card, index) => {
        if (index >= INITIAL_VISIBLE_CARDS) {
            card.style.display = "none";
        }
    });

    // Показываем все карточки при клике на кнопку
    const showAllCards = (): void => {
        appealCards.forEach((card) => {
            card.style.display = "flex";
        });

        // Скрываем кнопку и градиент
        loadMoreButton.style.display = "none";
        gradientContainer.style.display = "none";
    };

    // Назначаем обработчик на кнопку
    loadMoreButton.addEventListener("click", showAllCards);

    // Если карточек 8 или меньше, скрываем кнопку сразу
    if (appealCards.length <= INITIAL_VISIBLE_CARDS) {
        loadMoreButton.style.display = "none";
        gradientContainer.style.display = "none";
    }
});

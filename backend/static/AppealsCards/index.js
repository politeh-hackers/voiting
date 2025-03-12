document.addEventListener("DOMContentLoaded", function () {
    var loadMoreButton = document.getElementById("load-more-button");
    var gradientContainer = document.querySelector(".gradient-container");
    var appealCards = document.querySelectorAll(".card__appeal");
    var INITIAL_VISIBLE_CARDS = 8;
    // Скрываем все карточки после 8-й
    appealCards.forEach(function (card, index) {
        if (index >= INITIAL_VISIBLE_CARDS) {
            card.style.display = "none";
        }
    });
    // Показываем все карточки при клике на кнопку
    var showAllCards = function () {
        appealCards.forEach(function (card) {
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

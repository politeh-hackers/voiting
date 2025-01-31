document.addEventListener('DOMContentLoaded', function () {
    var loadMoreButton = document.getElementById('load-more-button');
    var gradientContainer = document.querySelector('.gradient-container');
    var appealCards = document.querySelectorAll('.card__appeal');
    var visibleCount = 8;
    var showNextCards = function () {
        for (var i = visibleCount; i < visibleCount + 8 && i < appealCards.length; i++) {
            appealCards[i].style.display = 'flex';
            appealCards[i].offsetHeight;
        }
        visibleCount += 8;
        if (visibleCount >= appealCards.length) {
            loadMoreButton.style.display = 'none';
            gradientContainer.style.display = 'none'; // Скрываем градиент, когда кнопка скрыта
        }
    };
    for (var i = 0; i < visibleCount && i < appealCards.length; i++) {
        appealCards[i].style.display = 'flex';
        appealCards[i].offsetHeight;
    }
    loadMoreButton.addEventListener('click', showNextCards);
    if (appealCards.length <= visibleCount) {
        loadMoreButton.style.display = 'none';
        gradientContainer.style.display = 'none'; // Скрываем градиент, если кнопка скрыта
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const loadMoreButton = document.getElementById('load-more-button') as HTMLButtonElement;
    const gradientContainer = document.querySelector('.gradient-container') as HTMLElement;
    const appealCards = document.querySelectorAll('.card__appeal') as NodeListOf<HTMLElement>;
    let visibleCount = 8;

    const showNextCards = (): void => {
        for (let i = visibleCount; i < visibleCount + 8 && i < appealCards.length; i++) {
            appealCards[i].style.display = 'flex';
            appealCards[i].offsetHeight;
        }
        visibleCount += 8;

        if (visibleCount >= appealCards.length) {
            loadMoreButton.style.display = 'none';
            gradientContainer.style.display = 'none'; // Скрываем градиент, когда кнопка скрыта
        }
    };

    for (let i = 0; i < visibleCount && i < appealCards.length; i++) {
        appealCards[i].style.display = 'flex';
        appealCards[i].offsetHeight;
    }

    loadMoreButton.addEventListener('click', showNextCards);

    if (appealCards.length <= visibleCount) {
        loadMoreButton.style.display = 'none';
        gradientContainer.style.display = 'none'; // Скрываем градиент, если кнопка скрыта
    }
});
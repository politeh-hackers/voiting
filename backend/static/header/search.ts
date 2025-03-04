interface SearchResult {
    type: 'biography' | 'media' | 'actual' | 'appeals';
    id: number;
    header?: string;
    summary?: string;
    text?: string;
    title?: string;
}

interface SearchResponse {
    results: SearchResult[];
}

document.addEventListener('DOMContentLoaded', (): void => {
    const searchButton: HTMLElement | null = document.getElementById('searchButton');
    const searchPopup: HTMLElement | null = document.getElementById('searchPopup');
    const searchInput: HTMLInputElement | null = document.querySelector('.input__search');
    const clearButton: HTMLElement | null = document.getElementById('clearButton');
    let searchTimeout: number;

    if (!searchButton || !searchPopup || !searchInput || !clearButton) {
        console.error('Не удалось найти необходимые элементы поиска');
        return;
    }

    // Открытие/закрытие поиска
    searchButton.addEventListener('click', (): void => {
        searchPopup.classList.toggle('active');
        if (searchPopup.classList.contains('active')) {
            searchInput.focus();
        }
    });

    // Очистка поиска
    clearButton.addEventListener('click', (): void => {
        searchInput.value = '';
        searchInput.focus();
        updateSearchResults([]);
    });

    // Обработка ввода в поиск
    searchInput.addEventListener('input', (e: Event): void => {
        const target = e.target as HTMLInputElement;
        clearTimeout(searchTimeout);
        const query: string = target.value.trim();
        
        if (query.length < 2) {
            updateSearchResults([]);
            return;
        }

        searchTimeout = setTimeout((): void => {
            fetch(`/search/?q=${encodeURIComponent(query)}`)
                .then((response: Response) => response.json())
                .then((data: SearchResponse) => {
                    updateSearchResults(data.results);
                })
                .catch((error: Error) => {
                    console.error('Ошибка поиска:', error);
                    updateSearchResults([]);
                });
        }, 300);
    });

    // Обновление результатов поиска
    function updateSearchResults(results: SearchResult[]): void {
        if (!searchPopup) return;
        
        const resultsContainer: HTMLDivElement = document.createElement('div');
        resultsContainer.className = 'search-results';

        if (results.length === 0) {
            resultsContainer.innerHTML = '<div class="no-results">Ничего не найдено</div>';
        } else {
            results.forEach((result: SearchResult) => {
                const resultItem: HTMLDivElement = document.createElement('div');
                resultItem.className = 'search-result-item';

                if (result.type === 'media' || result.type === 'actual') {
                    resultItem.innerHTML = `
                        <h3>${result.header}</h3>
                        <p>${result.summary}</p>
                    `;
                } else if (result.type === 'appeals') {
                    resultItem.innerHTML = `
                        <h3>${result.title}</h3>
                        <p>${result.text}</p>
                    `;
                }

                resultItem.addEventListener('click', (): void => {
                    window.location.href = `/${result.type}/${result.id}`;
                });
                resultsContainer.appendChild(resultItem);
            });
        }

        // Удаляем старые результаты
        const oldResults: Element | null = searchPopup.querySelector('.search-results');
        if (oldResults) {
            oldResults.remove();
        }

        // Добавляем новые результаты
        searchPopup.appendChild(resultsContainer);
    }
}); 
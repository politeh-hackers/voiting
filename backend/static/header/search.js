document.addEventListener('DOMContentLoaded', function () {
    var searchButton = document.getElementById('searchButton');
    var searchPopup = document.getElementById('searchPopup');
    var searchInput = document.querySelector('.input__search');
    var clearButton = document.getElementById('clearButton');
    var searchTimeout;
    if (!searchButton || !searchPopup || !searchInput || !clearButton) {
        console.error('Не удалось найти необходимые элементы поиска');
        return;
    }
    // Открытие/закрытие поиска
    searchButton.addEventListener('click', function () {
        searchPopup.classList.toggle('active');
        if (searchPopup.classList.contains('active')) {
            searchInput.focus();
        }
    });
    // Очистка поиска
    clearButton.addEventListener('click', function () {
        searchInput.value = '';
        searchInput.focus();
        updateSearchResults([]);
    });
    // Обработка ввода в поиск
    searchInput.addEventListener('input', function (e) {
        var target = e.target;
        clearTimeout(searchTimeout);
        var query = target.value.trim();
        if (query.length < 2) {
            updateSearchResults([]);
            return;
        }
        searchTimeout = setTimeout(function () {
            fetch("/search/?q=".concat(encodeURIComponent(query)))
                .then(function (response) { return response.json(); })
                .then(function (data) {
                updateSearchResults(data.results);
            })
                .catch(function (error) {
                console.error('Ошибка поиска:', error);
                updateSearchResults([]);
            });
        }, 300);
    });
    // Обновление результатов поиска
    function updateSearchResults(results) {
        if (!searchPopup)
            return;
        var resultsContainer = document.createElement('div');
        resultsContainer.className = 'search-results';
        if (results.length === 0) {
            resultsContainer.innerHTML = '<div class="no-results">Ничего не найдено</div>';
        }
        else {
            results.forEach(function (result) {
                var resultItem = document.createElement('div');
                resultItem.className = 'search-result-item';
                if (result.type === 'media' || result.type === 'actual') {
                    resultItem.innerHTML = "\n                        <h3>".concat(result.header, "</h3>\n                        <p>").concat(result.summary, "</p>\n                    ");
                }
                else if (result.type === 'appeals') {
                    resultItem.innerHTML = "\n                        <h3>".concat(result.title, "</h3>\n                        <p>").concat(result.text, "</p>\n                    ");
                }
                resultItem.addEventListener('click', function () {
                    window.location.href = "/".concat(result.type, "/").concat(result.id);
                });
                resultsContainer.appendChild(resultItem);
            });
        }
        // Удаляем старые результаты
        var oldResults = searchPopup.querySelector('.search-results');
        if (oldResults) {
            oldResults.remove();
        }
        // Добавляем новые результаты
        searchPopup.appendChild(resultsContainer);
    }
});

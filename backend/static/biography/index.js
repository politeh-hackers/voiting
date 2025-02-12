document.addEventListener("DOMContentLoaded", function () {
    var slides = document.querySelectorAll(".main-photo-slide");
    var sections = document.querySelectorAll(".media__page-container");
    var currentIndex = 0;
    // Функция для смены слайда
    var changeSlide = function (index) {
        slides.forEach(function (slide, i) {
            slide.classList.toggle("active", i === index);
        });
    };
    // Создаем Intersection Observer
    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                var index = Array.from(sections).indexOf(entry.target);
                if (index !== currentIndex) {
                    currentIndex = index;
                    changeSlide(index);
                }
            }
        });
    }, { threshold: 0.3 });
    // Наблюдаем за всеми секциями
    sections.forEach(function (section) { return observer.observe(section); });
    // Показываем первый слайд сразу
    changeSlide(0);
});
document.addEventListener("DOMContentLoaded", function () {
    var dateLinks = document.querySelectorAll(".date-link");
    var sections = document.querySelectorAll(".media__page-container");
    var maxVisible = 6; // Максимум 6 видимых дат
    var updateActiveDate = function (index) {
        dateLinks.forEach(function (link, i) {
            var distance = Math.abs(i - index);
            if (distance === 0) {
                // Активная дата (красная, большая)
                link.classList.add("active");
                link.classList.remove("nearby", "far");
                link.style.fontSize = "24px";
                link.style.color = "#EA424C";
            }
            else if (distance === 1) {
                // Ближайшие даты (черные, средние)
                link.classList.remove("active", "far");
                link.classList.add("nearby");
                link.style.fontSize = "20px";
                link.style.color = "black";
            }
            else if (distance === 2) {
                // Даты дальше (серые, маленькие)
                link.classList.remove("active", "nearby");
                link.classList.add("nearby");
                link.style.fontSize = "16px";
                link.style.color = "#aaa";
            }
            else {
                // Остальные скрываем
                link.style.display = "none";
                return;
            }
            // Показываем только максимум 6 элементов
            link.style.display = "block";
        });
    };
    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                var index = Array.from(sections).indexOf(entry.target);
                if (index !== -1) {
                    updateActiveDate(index);
                }
            }
        });
    }, { threshold: 0.3 });
    sections.forEach(function (section) { return observer.observe(section); });
    // Устанавливаем начальное состояние
    updateActiveDate(0);
});

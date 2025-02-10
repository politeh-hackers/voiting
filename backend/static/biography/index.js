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
    }, { threshold: 0.5 });
    // Наблюдаем за всеми секциями
    sections.forEach(function (section) { return observer.observe(section); });
    // Показываем первый слайд сразу
    changeSlide(0);
});

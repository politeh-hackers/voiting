document.addEventListener("DOMContentLoaded", () => {
  const slides: NodeListOf<HTMLElement> = document.querySelectorAll(".main-photo-slide");
  const sections: NodeListOf<HTMLElement> = document.querySelectorAll(".media__page-container");
  let currentIndex: number = 0;

  // Функция для смены слайда
  const changeSlide = (index: number): void => {
      slides.forEach((slide, i) => {
          slide.classList.toggle("active", i === index);
      });
  };

  // Создаем Intersection Observer
  const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
          if (entry.isIntersecting) {
              const index: number = Array.from(sections).indexOf(entry.target as HTMLElement);
              if (index !== currentIndex) {
                  currentIndex = index;
                  changeSlide(index);
              }
          }
      });
  }, { threshold: 0.3 });

  // Наблюдаем за всеми секциями
  sections.forEach(section => observer.observe(section));

  // Показываем первый слайд сразу
  changeSlide(0);
});
document.addEventListener("DOMContentLoaded", () => {
    const dateLinks: NodeListOf<HTMLAnchorElement> = document.querySelectorAll(".date-link");
    const sections: NodeListOf<HTMLElement> = document.querySelectorAll(".media__page-container");
    const maxVisible = 6; // Максимум 6 видимых дат

    const updateActiveDate = (index: number) => {
        dateLinks.forEach((link, i) => {
            const distance = Math.abs(i - index);

            if (distance === 0) {
                // Активная дата (красная, большая)
                link.classList.add("active");
                link.classList.remove("nearby", "far");
                link.style.fontSize = "24px";
                link.style.color = "#EA424C";
            } else if (distance === 1 ) {
                // Ближайшие даты (черные, средние)
                link.classList.remove("active", "far");
                link.classList.add("nearby");
                link.style.fontSize = "20px";
                link.style.color = "black";
            } else if (distance === 2 ) {
                // Даты дальше (серые, маленькие)
                link.classList.remove("active", "nearby");
                link.classList.add("nearby");
                link.style.fontSize = "16px";
                link.style.color = "#aaa";
            } else {
                // Остальные скрываем
                link.style.display = "none";
                return;
            }

            // Показываем только максимум 6 элементов
            link.style.display = "block";
        });
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                const index = Array.from(sections).indexOf(entry.target as HTMLElement);
                if (index !== -1) {
                    updateActiveDate(index);
                }
            }
        });
    }, { threshold: 0.3 });

    sections.forEach(section => observer.observe(section));

    // Устанавливаем начальное состояние
    updateActiveDate(0);
});


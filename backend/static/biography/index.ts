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
  }, { threshold: 0.5 });

  // Наблюдаем за всеми секциями
  sections.forEach(section => observer.observe(section));

  // Показываем первый слайд сразу
  changeSlide(0);
});

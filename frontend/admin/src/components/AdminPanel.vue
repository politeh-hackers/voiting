<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import SpeedDial from 'primevue/speeddial';
import 'primeicons/primeicons.css';
import Button from "primevue/button";

const router = useRouter();

const menuItems = [
  { label: "Категории", route: "/Form", icon: "pi pi-folder" },
  { label: "Медиа", route: "/Media", icon: "pi pi-image" },
  { label: "Обращения", route: "/Appeals", icon: "pi pi-envelope" },
  { label: "Актуальное", route: "/Actual", icon: "pi pi-calendar" },
  { label: "Добавить админа", route: "/Admin", icon: "pi pi-user" }
];

const additionalItems = [
  { label: 'Добавить админа', route: "/Admin", icon: 'pi pi-user' },
  { label: 'Теги', route: "/Tags", icon: 'pi pi-hashtag' }
];

const activeRoute = ref(router.currentRoute.value.path);

const setActiveRoute = (route: string) => {
  activeRoute.value = route;
  router.push(route);
};

const sidebarVisible = ref(false);

const toggleSidebar = () => {
  sidebarVisible.value = !sidebarVisible.value;
  if (sidebarVisible.value) {
    document.body.style.overflow = "hidden"; // Блокируем прокрутку страницы при открытой панели
  } else {
    document.body.style.overflow = "auto"; // Включаем прокрутку страницы
  }
};
</script>

<template>
  <div class="main__menu">
    <!-- Верхняя панель с логотипом и кнопкой для меню -->
    <div class="header">
      <Button class="menu_button" icon="pi pi-bars" @click="toggleSidebar" />
      <div class="logo">
        <img src="./123.svg" alt="Logo" />
      </div>
    </div>

    <div class="container" :class="{ 'sidebar-open': sidebarVisible }">
      <!-- Левая панель с кнопками (показывается или скрывается) -->
      <transition name="sidebar-slide">
        <div v-if="sidebarVisible" class="sidebar">
          <div class="custom-menu">
            <div
              v-for="item in menuItems" :key="item.route"
              :class="{ 'menu-item': true, active: activeRoute === item.route }"
              @click="setActiveRoute(item.route)"
            >
              <i :class="item.icon" class="menu-icon"></i>
              <span>{{ item.label }}</span>
            </div>
          </div>
        </div>
      </transition>

      <!-- Правая область для отображения содержимого -->
      <div class="content">
        <!-- Использование items для SpeedDial -->
        <RouterView />
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Стили для верхней панели */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: black;
  color: white;
}

.logo img {
  height: 22px;
}

/* Основной контейнер */
.container {
  display: flex;
  height: calc(100vh - 60px); /* Высота экрана минус высота верхней панели */
  background-color: white;
  margin: 0;
  padding: 0;
  transition: transform 0.3s ease;
}

/* Левая панель */
.sidebar {
  width: 260px;
  background-color: black;
  display: flex;
  flex-direction: column;
  gap: 20px;
  border-right: 2px solid #e5e7eb;
  height: 100%;
  position: fixed;
  left: -260px; /* Скрываем панель по умолчанию за пределами экрана */
  z-index: 10;
  opacity: 0; /* Начинаем с нулевой видимости */
  transition: transform 0.3s ease, opacity 0.3s ease;
}

/* Стиль для кнопки в меню */
.menu-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 15px;
  color: white;
  cursor: pointer;
  font-family: Arial, sans-serif;
  font-size: 1rem;
  transition: all 0.3s ease;
  text-align: left;
}

.menu-item:hover {
  background-color: white;
  color: black;
}

.menu-item.active {
  background-color: white;
  color: black;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Правая область */
.content {
  flex-grow: 1;
  padding: 20px;
  background-color: white;
  overflow-y: auto;
  transition: margin-left 0.3s ease; /* Плавный сдвиг содержимого */
}

/* Переходы для анимации панели */
.sidebar-slide-enter-active{
  transition: transform 0.6s ease, opacity 0.6s ease;
}
.sidebar-slide-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.sidebar-slide-enter, .sidebar-slide-leave-to /* .sidebar-slide-leave-active in <2.1.8 */ {
  transform: translateX(-100%);
  opacity: 0;
}

/* Когда панель открыта, контент сдвигается */
.container.sidebar-open .sidebar {
  transform: translateX(260px); /* Сдвигаем панель в пределах экрана */
  opacity: 1; /* Панель становится видимой */
}

.container.sidebar-open .content {
  margin-left: 260px; /* Сдвигаем контент, когда панель открыта */
}
</style>

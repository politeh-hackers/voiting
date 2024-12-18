<script setup lang="ts">
import { ref } from "vue";
import Toolbar from 'primevue/toolbar';
import Button from "primevue/button";
import Menu from "primevue/menu";
import 'primeicons/primeicons.css';
import { RouterLink, RouterView, useRouter } from "vue-router";
import { InputIcon } from "primevue";
import { IconField } from "primevue";
import { SplitButton } from "primevue";
import { Avatar } from "primevue";
import SpeedDial from 'primevue/speeddial';

const router = useRouter();
const items = ref([
  { label: "Категории", command: () => router.push("/Form") },
  { label: "Медиа", command: () => router.push("/Media") },
  { label: "Обращения", command:()=> router.push("/Appeals") },
  { label: "Актуальное", command:() => router.push("/Actual") },
]);

const items2 = ref([
  { label: 'Добавить админа', command: () => router.push("/Admin"), icon: 'pi pi-user' },
  { label: 'Теги', icon: 'pi pi-hashtag'}
]);
const activeRoute = ref(""); // Отслеживаем активный маршрут
const setActiveRoute = (route: string) => {
  activeRoute.value = route;
  router.push(route);
};
</script>

<template>
  <div class="main__menu">
    <div class="container">
      <!-- Левая панель с кнопками -->
      <div class="sidebar">
        <img src = "https://1000logos.net/wp-content/uploads/2017/05/Pepsi-logo.png" class="welcome__text"></img>
        <div class="custom-menu">
          <div 
            class="menu-item"
            :class="{ active: activeRoute === '/Form' }"
            @click="setActiveRoute('/Form')"
          >
            <i class="pi pi-folder menu-icon"></i>
            <span>Категории</span>
          </div>
          <div 
            class="menu-item"
            :class="{ active: activeRoute === '/Media' }"
            @click="setActiveRoute('/Media')"
          >
            <i class="pi pi-image menu-icon"></i>
            <span>Медиа</span>
          </div>
          <div 
            class="menu-item"
            :class="{ active: activeRoute === '/Appeals' }"
            @click="setActiveRoute('/Appeals')"
          >
            <i class="pi pi-envelope menu-icon"></i>
            <span>Обращения</span>
          </div>
          <div 
            class="menu-item"
            :class="{ active: activeRoute === '/Actual' }"
            @click="setActiveRoute('/Actual')"
          >
            <i class="pi pi-calendar menu-icon"></i>
            <span>Актуальное</span>
          </div>
        </div>
      </div>
      <!-- Правая область для отображения содержимого -->
      <div class="content">
        <div class="card">
          <div>
            <SpeedDial :model="items2" direction="up" style="position: absolute; left: calc(2%); bottom: 3%;" />
             
            
          </div>
        </div>
        <RouterView />
      </div>
    </div>
  </div>
</template>

<style scoped>
.welcome__text {
  width: 100px;
}
.custom-menu {
  display: flex;
  flex-direction: column;
  gap: 0px;
  width: 100%;
  padding: 0 ;
}
.menu-item {
  background-color: black; /* Темно-синий фон кнопки */
  color: white; /* Желтый текст */
  padding: 15px;
  border-radius: 0px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-family: Arial, sans-serif;
  font-size: 1rem;
  transition: all 0.3s ease;
  text-align: left;
  
}
.menu-item:hover {
  background-color: white; /* Желтая подсветка */
  color: black; /* Темно-синий текст */
}
/* Основной контейнер */
.container {
  display: flex;
  margin: 0;
  padding: 0;
  background-color: wheat;
  height: 100vh; /* Высота 100% экрана */
}
.menu-item.active {
  background-color: white; /* Желтый фон для активной кнопки */
  color: black; /* Темно-синий текст */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  
}
/* Левая панель */
.sidebar {
  width: 20%;
  background-color: black; /* Темно-синий фон */
  display: flex;
  flex-direction: column;
  gap: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);
  align-items: center;
  padding: 20px 0;
  margin: 0;
  border-right: 2px solid #e5e7eb; /* Светло-серая разделительная линия */
}

/* Правая область */
.content {
  width: 80%;
  padding: 20px;
  overflow-y: auto;
  background-color: #fff;
}
h1 {
  margin: 0;
  padding: 0;
}
.sidebar .menu__panel {
  width: 100%;
  margin: 0;
  padding: 0;
}


</style>
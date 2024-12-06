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
  { label: "Актуальное" },
]);

const items2 = ref([
  { label: 'Добавить админа', command: () => router.push("/Admin"), icon: 'pi pi-user' },
  { label: 'Теги', icon: 'pi pi-hashtag'}
]);


</script>

<template>
  <div class="main__menu">
    <div class="container">
      <!-- Левая панель с кнопками -->
      <div class="sidebar">
        <h1 class="welcome__text">Admin panel</h1>
        <div class="menu__panel">
          <Menu :model="items" />
        </div>
      </div>
      <!-- Правая область для отображения содержимого -->
      <div class="content">
        <div class="card">
      <div>
          <SpeedDial :model="items2" direction="up" style="position: absolute; left: calc(2%); bottom: 3%" />
      </div>
  </div>
        <RouterView />
      </div>
    </div>
  </div>
</template>

<style scoped>
.welcome__text {
  font-family: "Gill Sans", "Gill Sans MT", Calibri, "Trebuchet MS", sans-serif;
  color: green;
  margin: 0;
  padding: 20px;
}
/* Основной контейнер */
.container {
  display: flex;
  margin: 0;
  padding: 0;
  background-color: wheat;
  height: 100vh; /* Высота 100% экрана */
}

/* Левая панель */
.sidebar {
  width: 20%;
  background-color: #f4f4f4;
  
  display: flex;
  flex-direction: column;
  gap: 10px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  align-items: center;
  gap: 30px;
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
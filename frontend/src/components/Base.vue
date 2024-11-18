<script setup lang="ts">
import { ref } from "vue";
import Button from "primevue/button";
import { RouterLink, RouterView, useRouter } from "vue-router";
const router = useRouter();
</script>

<template>
  <div class="main__menu">
    <div class="container">
      <!-- Левая панель с кнопками -->
      <div class="sidebar">
        <h1 class="welcome__text">Admin panel</h1>
        <RouterLink to="/Form">
          <Button label="Обращения" class="p-button-success" />
        </RouterLink>

      </div>
      <!-- Правая область для отображения содержимого -->
      <div class="content">
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
  padding: 0;
  
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
  width: 30%; /* Занимает 30% ширины */
  background-color: #f4f4f4; /* Светлый фон */
  padding: 20px;
  display: flex;
  flex-direction: column; /* Кнопки располагаются вертикально */
  gap: 10px; /* Отступы между кнопками */
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  align-items: center;
  gap: 30px;
}

/* Правая область */
.content {
  width: 70%; /* Занимает 70% ширины */
  padding: 20px;
  overflow-y: auto; /* Скроллинг, если контент слишком длинный */
  background-color: #fff;
}
h1{
  margin: 0;
  padding: 0;
}
</style>
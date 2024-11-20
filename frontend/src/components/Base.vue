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
  padding: 0px;
 
  
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
  padding: 20px;
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
h1{
  margin: 0;
  padding: 0;
}

</style>
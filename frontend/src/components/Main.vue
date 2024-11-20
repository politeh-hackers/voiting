<script setup lang="ts">
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import {ref} from 'vue'
import { useRouter } from 'vue-router';
const router = useRouter();
const text = ref('')
const text1 = ref('')
const correctUsername = 'admin';
const correctPassword = '12345';
const login = () => {
  if (text.value === correctUsername && text1.value === correctPassword) {
    // Если данные введены верно, переходим на страницу dashboard
    router.push({name:'Base'})
  } else {
    // Если данные неверные, можно показать ошибку
    alert('Неверное имя пользователя или пароль');
  }
};
</script>

<template>
  <div class="main__menu">
    <span class="main__text">Admin panel</span>
    <InputText v-model="text" name="login" placeholder="Login"/>
    <InputText v-model="text1" name="password" placeholder="password" type="password"/>
    <Button label="Log in" @click="login"/>
  </div>
</template>

<style scoped>
.main__menu{
  font-family:'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap:30px;
  height: 100vh;
  background-image: url(https://images.unsplash.com/photo-1708549566274-638eb2d2108b?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxleHBsb3JlLWZlZWR8MTd8fHxlbnwwfHx8fHw%3D) ;
  background-size: cover;        /* Растягивает изображение на весь экран */
  background-repeat: no-repeat;  /* Убирает повторение изображения */
  background-position: center;
}
.main__text {
  font-size: 24px;
}

</style>
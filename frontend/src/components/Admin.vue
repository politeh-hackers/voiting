<script setup lang="ts">
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Message from 'primevue/message';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();

const formState = ref({
  login: '',
  password: '',
  errorMessage: '',
  successMessage: '',
});

const register = async () => {
  formState.value.errorMessage = '';
  formState.value.successMessage = '';

  try {
    const response = await axios.post('http://127.0.0.1:8000/admin/registration', {
      login: formState.value.login,
      password: formState.value.password,
    });

    if (response.data.success) {
      formState.value.successMessage = 'Регистрация успешна!';
      formState.value.errorMessage = '';

      setTimeout(() => {
        router.push({ name: 'Base' });
      }, 1000);
    } else {
      // Отображаем ошибки, полученные от сервера
      formState.value.errorMessage = response.data.message;
    }
  } catch (error) {
    formState.value.errorMessage = 'Ошибка подключения к серверу.';
    console.error('Ошибка:', error);
  }
};
</script>

<template>
  <div class="main__menu">
    <form @submit.prevent="register" class="form">
      <div class="form-group">
        <InputText v-model="formState.login" type="text" placeholder="Логин" />
      </div>
      <div class="form-group">
        <InputText v-model="formState.password" type="password" placeholder="Пароль" />
      </div>
      <div class="form-group message-container">
        <!-- Показываем сообщение об ошибке, если оно есть -->
        <Message 
          v-if="formState.errorMessage" 
          severity="error" 
          size="small" 
          variant="simple">
          {{ formState.errorMessage }}
        </Message>
        
        <!-- Показываем сообщение об успехе, если оно есть -->
        <Message 
          v-if="formState.successMessage" 
          severity="success" 
          size="small" 
          variant="simple">
          {{ formState.successMessage }}
        </Message>
      </div>
      <Button type="submit" label="Зарегистрироваться" />
    </form>
  </div>
</template>

<style scoped>
.main__menu {
  font-family: 'Franklin Gothic Medium', 'Arial Narrow', Arial, sans-serif;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 30px;
  height: 100vh;
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 300px;
}

.form-group {
  display: flex;
  flex-direction: column;
  position: relative;
}

.message-container {
  min-height: 20px;
}
</style>

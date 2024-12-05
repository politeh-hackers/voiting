<script setup lang="ts">
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Message from 'primevue/message';
import { ref } from 'vue';
import axios from 'axios';

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
    const response = await axios.post('http://127.0.0.1:8000/register/', {
      login: formState.value.login,
      password: formState.value.password,
    });

    if (response.data.success) {
      formState.value.successMessage = 'Регистрация успешна!';
      formState.value.errorMessage = '';
    } else {
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
        <Message v-if="formState.errorMessage" severity="error" size="small" variant="simple">
          {{ formState.errorMessage }}
        </Message>
        <Message v-if="formState.successMessage" severity="success" size="small" variant="simple">
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

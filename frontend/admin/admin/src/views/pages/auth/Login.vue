<script setup>
import FloatingConfigurator from '@/components/FloatingConfigurator.vue';
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import Password from 'primevue/password';
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

const login = async () => {
  formState.value.errorMessage = '';
  formState.value.successMessage = '';

  // Проверка на пустые поля
  if (!formState.value.login || !formState.value.password) {
    formState.value.errorMessage = 'Пожалуйста, заполните все поля';
    return;
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/admin/login', {
      login: formState.value.login,
      password: formState.value.password,
    });

    if (response.data.refresh) {
      const token = response.data.refresh;
      localStorage.setItem('authToken', token);
      formState.value.successMessage = 'Авторизация успешна!';
      formState.value.errorMessage = '';
      setTimeout(() => {
        router.push({ name: 'media' });
      }, 1000);
    } else {
      formState.value.errorMessage = 'Неверный логин или пароль';
    }
  } catch (error) {
    if (error.response && error.response.status === 401) {
      formState.value.errorMessage = 'Неверный логин или пароль';
    } else {
      formState.value.errorMessage = 'Ошибка подключения к серверу';
    }
    console.error('Ошибка:', error);
  }
};
</script>

<template>
    <FloatingConfigurator />
    <div class="bg-surface-50 dark:bg-surface-950 flex items-center justify-center min-h-screen min-w-[100vw] overflow-hidden">
        <div class="flex flex-col items-center justify-center">
            <div style="border-radius: 56px; padding: 0.3rem; background: linear-gradient(180deg, var(--primary-color) 10%, rgba(33, 150, 243, 0) 30%)">
                <div class="w-full bg-surface-0 dark:bg-surface-900 py-20 px-8 sm:px-20" style="border-radius: 53px">
                    <div class="text-center mb-8">
                        <div class="text-surface-900 dark:text-surface-0 text-3xl font-medium mb-4">Добро пожаловать!</div>
                        <span class="text-muted-color font-medium">Авторизуйтесь, чтобы продолжить</span>
                    </div>
                    <form @submit.prevent="login">
                        <div>
                            <label for="login" class="block text-surface-900 dark:text-surface-0 text-xl font-medium mb-2">Логин</label>
                            <InputText id="login" type="text" placeholder="Введите логин" class="w-full md:w-[30rem] mb-8" v-model="formState.login" :disabled="formState.loading" />

                            <label for="password1" class="block text-surface-900 dark:text-surface-0 font-medium text-xl mb-2">Пароль</label>
                            <Password id="password1" v-model="formState.password" placeholder="Введите пароль" :toggleMask="true" class="mb-4" fluid :feedback="false" :disabled="formState.loading"></Password>

                            <Button label="Войти" class="w-full" type="submit" :loading="formState.loading"></Button>
                        </div>
                        <div class="message-container mt-4">
                            <Message 
                              v-if="formState.errorMessage" 
                              severity="error" 
                              :closable="false">
                              {{ formState.errorMessage }}
                            </Message>
                            <Message 
                              v-if="formState.successMessage" 
                              severity="success" 
                              :closable="false">
                              {{ formState.successMessage }}
                            </Message>
                        </div>
                    </form>


                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.pi-eye {
    transform: scale(1.6);
    margin-right: 1rem;
}

.pi-eye-slash {
    transform: scale(1.6);
    margin-right: 1rem;
}

.message-container {
  min-height: 20px;
}
</style>
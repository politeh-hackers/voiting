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
  confirmPassword: '',
  errorMessage: '',
  successMessage: '',
  loading: false
});

const register = async () => {
  formState.value.errorMessage = '';
  formState.value.successMessage = '';
  formState.value.loading = true;

  // Проверка на пустые поля
  if (!formState.value.login || !formState.value.password || !formState.value.confirmPassword) {
    formState.value.errorMessage = 'Пожалуйста, заполните все поля';
    formState.value.loading = false;
    return;
  }

  // Проверка совпадения паролей
  if (formState.value.password !== formState.value.confirmPassword) {
    formState.value.errorMessage = 'Пароли не совпадают';
    formState.value.loading = false;
    return;
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/admin/registration', {
      login: formState.value.login,
      password: formState.value.password
    });

    if (response.data.success) {
      formState.value.successMessage = 'Регистрация успешна!';
      formState.value.errorMessage = '';
      setTimeout(() => {
        router.push('/admin/home'); // Перенаправление на домашнюю страницу
      }, 2000);
    }
  } catch (error) {
    if (error.response && error.response.data.message) {
      formState.value.errorMessage = error.response.data.message;
    } else if (error.response && error.response.status === 409) {
      formState.value.errorMessage = 'Пользователь с таким логином уже существует';
    } else {
      formState.value.errorMessage = 'Ошибка при регистрации. Попробуйте позже.';
    }
    console.error('Ошибка:', error);
  } finally {
    formState.value.loading = false;
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
                        <div class="text-surface-900 dark:text-surface-0 text-3xl font-medium mb-4">Регистрация</div>
                        <span class="text-muted-color font-medium">Создайте новый аккаунт</span>
                    </div>
                    <form @submit.prevent="register">
                        <div>
                            <label for="login" class="block text-surface-900 dark:text-surface-0 text-xl font-medium mb-2">Логин</label>
                            <InputText id="login" type="text" placeholder="Придумайте логин" class="w-full md:w-[30rem] mb-8" v-model="formState.login" :disabled="formState.loading" />

                            <label for="password1" class="block text-surface-900 dark:text-surface-0 font-medium text-xl mb-2">Пароль</label>
                            <Password id="password1" v-model="formState.password" placeholder="Придумайте пароль" :toggleMask="true" class="mb-4" fluid :feedback="false" :disabled="formState.loading"></Password>

                            <label for="password2" class="block text-surface-900 dark:text-surface-0 font-medium text-xl mb-2">Подтверждение пароля</label>
                            <Password id="password2" v-model="formState.confirmPassword" placeholder="Повторите пароль" :toggleMask="true" class="mb-4" fluid :feedback="false" :disabled="formState.loading"></Password>

                            <Button label="Зарегистрироваться" class="w-full" type="submit" :loading="formState.loading"></Button>
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
<script setup lang="ts">
import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import {ref} from 'vue'
import { useRouter } from 'vue-router';
const router = useRouter();
const text = ref('')
const text1 = ref('')
// const correctUsername = 'admin';
// const correctPassword = '12345';
const login = () => {
    router.push({name:'Base'})
}
</script>

<template>
  <div class="main__menu">
    <span>Admin panel</span>
    <InputText v-model="text" name="login" placeholder="Login"/>
    <InputText v-model="text1" name="password" placeholder="password" type="password"/>
    <Button label="Log in" @click="login"/>
  </div>
</template>

<style scoped>
.main__menu{
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap:30px;
  height: 80vh;
}
</style>
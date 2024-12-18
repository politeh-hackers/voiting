<script setup lang="ts">

import InputText from 'primevue/inputtext';
import Button from 'primevue/button';
import {ref} from 'vue'
import { useRouter } from 'vue-router';
const router = useRouter();
router.replace('/');
</script>

<template>
  <div class="main__menu">
    <router-view></router-view>  
  </div>
</template>

<style scoped>

</style>

<template>
  <div class="content__main">
  <div class="header">
  <InputText v-model="text" placeholder="header" class="header__input"></InputText>
</div>
  <div>
    <!-- Контейнер для EditorJS -->
    <div ref="editorContainer" class="content-editor"></div>
  </div>
  <div class="date__picker">
    <DatePicker v-model="date" />
  </div>
</div>
</template>

<script setup lang="ts">
import InputText from 'primevue/inputtext';
import { onMounted, ref } from 'vue';
import { initEditor } from '../editor.js/editor-init'; // Импорт функции инициализации
import DatePicker from 'primevue/datepicker';
const text = ref('')
const date = ref();
// Ссылка на контейнер редактора
const editorContainer = ref<HTMLElement | null>(null);
// Экземпляр редактора
let editorInstance: any = null;

// Инициализация редактора при монтировании компонента
onMounted(() => {
  if (editorContainer.value) {
    const data = null; // Передайте сюда данные для редактора, если нужно

    // Инициализируем EditorJS
    editorInstance = initEditor(editorContainer.value, data);
  }
});

// Освобождение ресурсов перед удалением компонента

</script>

<style lang="scss">
/* Стили для редактора */
.content-editor {
  border: 1px solid #ccc;
  padding: 10px;
  min-height: 200px;
  
}
.header{
  
  display: flex;
  justify-content: center;
  align-items: center;
}
.header__input{
  width: 100%;
}
.content__main{
  display: flex; /* Добавляем flex-контейнер */
  flex-direction: column;
  gap: 10px;
}
</style>

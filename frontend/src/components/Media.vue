<template>
  <div class="content__main">
  <div class="header">
  <InputText v-model="post.header" placeholder="header" class="header__input"></InputText>
</div>
  <div>
    <!-- Контейнер для EditorJS -->
    <div ref="editorContainer" class="content-editor"  ></div>
  </div>
  <div class="date__picker">
    <DatePicker v-model="post.date_created" />
  </div>
  <!-- <InputText v-model="post.media_tags" placeholder="header" class="header__input"></InputText> -->
  <Button icon = "pi pi-check" @click="addPost"></Button>
</div>
</template>

<script setup lang="ts">
import { PostService, Post } from "../api/serviceformedia";
import InputText from 'primevue/inputtext';
import { onMounted, ref, watch } from 'vue';
import { initEditor } from '../editor.js/editor-init'; // Импорт функции инициализации
import DatePicker from 'primevue/datepicker';
import Button from 'primevue/button';

const post = ref<Post>({
  header: "",
  content: "",
  date_created: new Date(),
});

const postService = new PostService();
const baseAdmin = "admin";
const prefix = "media";

const addPost = async () => {
  // Сохранение текущего контента из редактора в post.content
  post.value.content = await editorInstance.save().then((data: any) => JSON.stringify(data));

  await postService.create(post.value, prefix, baseAdmin);

  // Очистка полей
  post.value.header = "";
  post.value.content = "";
  post.value.date_created = new Date();

  // Очистка редактора
  editorInstance.clear();
};

// Ссылка на контейнер редактора
const editorContainer = ref<HTMLElement | null>(null);
// Экземпляр редактора
let editorInstance: any = null;

// Инициализация редактора при монтировании компонента
onMounted(() => {
  if (editorContainer.value) {
    // Инициализация с текущим содержимым из post.content
    editorInstance = initEditor(editorContainer.value, JSON.parse(post.value.content || "{}"));
  }
});

// Наблюдение за изменением post.content
watch(
  () => post.value.content,
  (newContent) => {
    if (editorInstance) {
      // Обновление контента редактора при изменении post.content
      editorInstance.render(JSON.parse(newContent || "{}"));
    }
  }
);
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

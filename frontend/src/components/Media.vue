<template>
  <div class="card flex justify-center">
    <Button class="content__view" label="Добавить новость" @click="visible = true" />
    <Dialog v-model:visible="visible" @show="initializeEditor" modal header="Добавить новость" :style="{ width: '60rem' }">
      
      <div class="content__main">
      <div class="header">
        <InputText
          v-model="post.header"
          placeholder="header"
          class="header__input"
        ></InputText>
      </div>

      <!-- Контейнер для EditorJS -->
      <div ref="editorContainer" class="content-editor"></div>

      <div class="date__picker">
        <DatePicker v-model="post.date_created" />
      </div>
      <!-- <InputText v-model="post.media_tags" placeholder="header" class="header__input"></InputText> -->
      <Button icon="pi pi-check" @click="addPost"></Button>
    </div>
    </Dialog>
    
  </div>
</template>

<script setup lang="ts">
import { PostService, Post } from "../api/serviceformedia";
import InputText from "primevue/inputtext";
import { onMounted, ref, watch } from "vue";
import { initEditor } from "../editor.js/editor-init"; // Импорт функции инициализации
import DatePicker from "primevue/datepicker";
import Button from "primevue/button";
import Dialog from "primevue/dialog";

const post = ref<Post>({
  header: "",
  content: "",
  date_created: new Date(),
});

const postService = new PostService();
const baseAdmin = "admin";
const prefix = "test";

const visible = ref(false);
const addPost = async () => {
  // Save the current content from the editor into post.content
  post.value.content = await editorInstance
    .save()
    .then((data) => JSON.stringify(data));

  let content = new FormData();
  content.append("content", post.value.content);
  content.append("header", post.value.header);

  // Send the request using HTTP
  fetch("http://localhost:8000/admin/media", {
    method: "POST",
    body: content,
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      } else {
        throw new Error("Network response was not ok: " + response.statusText);
      }
    })
    .then((data) => {
      console.log("Success:", data); // Log the success response
    })
    .catch((error) => {
      console.error("Error:", error); // Handle any errors
    });

  // Clear fields
  post.value.header = "";
  post.value.content = "";
  post.value.date_created = new Date();

  // Clear the editor
  editorInstance.clear();
};

// Ссылка на контейнер редактора
const editorContainer = ref<HTMLElement | null>(null);
// Экземпляр редактора
let editorInstance: any = null;

// Инициализация редактора при монтировании компонента
const initializeEditor = () => {
  if (editorContainer.value) {
    console.log("Initializing editor...");
    editorInstance = initEditor(
      editorContainer.value,
      JSON.parse(post.value.content || "{}")
    );
  }
};

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
.header {
  display: flex;
  justify-content: center;
  align-items: center;
}
.header__input {
  width: 100%;
}
.content__main {
  display: flex; /* Добавляем flex-контейнер */
  flex-direction: column;
  gap: 10px;
}
.content__view{
  width: 100%;
}
</style>

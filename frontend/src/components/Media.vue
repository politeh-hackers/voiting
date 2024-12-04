<template>
  <div class="card flex flex-column">
    <Button
      class="content__view"
      label="Добавить новость"
      @click="visible = true"
    />
    <Dialog
      v-model:visible="visible"
      @show="initializeEditor"
      modal
      header="Добавить новость"
      :style="{ width: '60rem' }"
    >
      <div class="content__main">
        <div class="header">
          <InputText
            v-model="post.header"
            placeholder="Заголовок"
            class="header__input"
          />
        </div>
        <div class="summary">
          <InputText
            v-model="post.summary"
            placeholder="Краткое описание"
            class="summary_input"
          />
        </div>

        <!-- Используем компонент FileUpload для загрузки изображения -->
        <div class="image-upload">
          <label for="image-upload">Загрузить изображение:</label>
          <FileUpload
            name="main_photo"
            :url="'http://localhost:8000/admin/image'" 
            accept="image/*"
            :auto="true"
            @upload="onImageUpload"
            chooseLabel="Выбрать изображение"
          />
        </div>

        <div ref="editorContainer" class="content-editor"></div>

        <div class="date__picker">
          <DatePicker v-model="post.date_created" />
        </div>

        <Button icon="pi pi-check" @click="addPost" />
      </div>
    </Dialog>

    <!-- DataView для отображения списка новостей -->
    <DataView :value="newsList" paginator :rows="5" dataKey="'id'">
      <template #list="slotProps">
        <div class="news-container">
          <div v-for="(newsItem, index) in slotProps.items" :key="newsItem.id">
            <div class="news-item" :class="{ 'border-top': index !== 0 }">
              <!-- Контент новости слева -->
              <div class="news-info">
                <div class="news-header">
                  <span class="news-date">
                    {{ new Date(newsItem.date_created).toLocaleDateString() }}
                  </span>
                  <div class="news-title">{{ newsItem.header }}</div>
                </div>

              </div>

              <!-- Изображение новости справа -->
              <div class="image-container">
                <!-- Проверка на наличие изображения в контенте -->
                <img 
                  v-if="newsItem.main_photo" 
                  class="news-image" 
                  :src="`http://localhost:8000/static/images/${newsItem.main_photo}`" 
                  :alt="newsItem.header"
                />
                <div v-if="newsItem.main_photo" class="tag-overlay">
                  <Tag :value="'News'" severity="info"></Tag>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </DataView>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import InputText from "primevue/inputtext";
import DatePicker from "primevue/datepicker";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import DataView from "primevue/dataview";
import FileUpload from "primevue/fileupload"; // Импортируем компонент FileUpload
import { PostService, Post } from "../api/serviceformedia";
import { initEditor } from "../editor.js/editor-init";

const post = ref<Post>({
  summary: "",
  main_photo: "",
  header: "",
  content: "",
  date_created: new Date(),
});

const visible = ref(false);
const editorContainer = ref<HTMLElement | null>(null);
let editorInstance: any = null;

const newsList = ref<Post[]>([]); // Список новостей
const postService = new PostService();

// Функция для обработки загрузки изображения
const onImageUpload = (event: any) => {
  // При успешной загрузке изображения
  const uploadedImage = event.files[0];
  if (uploadedImage) {
    post.value.main_photo = uploadedImage.name; // Сохраняем имя изображения в объект post
  }
};

const renderBlocks = (content: string): string => {
  try {
    const parsedContent = JSON.parse(content);

    if (parsedContent.blocks && Array.isArray(parsedContent.blocks)) {
      return parsedContent.blocks
        .map((block) => {
          if (block.type === "image" && block.data.file && block.data.file.url) {
            return `<img src="${block.data.file.url}" alt="image" style="max-width: 100%; margin-bottom: 10px;" />`;
          }
          return "";
        })
        .join("");
    }
  } catch (error) {
    console.error("Error parsing content:", error);
  }
  return "";
};

// Загрузка списка новостей
const loadNews = async () => {
  try {
    const response = await fetch("http://localhost:8000/admin/media");
    if (response.ok) {
      newsList.value = await response.json();
    } else {
      console.error("Failed to load news:", response.statusText);
    }
  } catch (error) {
    console.error("Error loading news:", error);
  }
};

const addPost = async () => {
  post.value.content = await editorInstance
    .save()
    .then((data) => JSON.stringify(data));

  const content = new FormData();
  content.append("content", post.value.content);
  content.append("header", post.value.header);

  // Добавление изображения, если оно есть
  if (post.value.main_photo) {
    content.append("main_photo", post.value.main_photo);
  }

  try {
    const response = await fetch("http://localhost:8000/admin/media", {
      method: "POST",
      body: content,
    });

    if (response.ok) {
      console.log("Post added successfully");
      loadNews(); // Обновление списка новостей
      post.value.header = "";
      visible.value = false; // Закрытие формы
    } else {
      console.error("Error adding post:", response.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
  }
};

const initializeEditor = () => {
  if (editorContainer.value) {
    editorInstance = initEditor(editorContainer.value, {});
  }
};

onMounted(() => {
  loadNews(); // Загрузка новостей при монтировании
});
</script>

<style lang="scss">
.content-editor {
  border: 1px solid #ccc;
  padding: 10px;
  min-height: 200px;
}

.news-container {
  display: flex;
  flex-direction: column;
}

.news-item {
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  gap: 1rem;
}

.border-top {
  border-top: 1px solid #e0e0e0;
}

.news-info {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
}

.news-header {
  display: flex;
  flex-direction: column;
}

.news-date {
  font-size: 0.875rem;
  color: #888;
}

.news-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 0.5rem;
}

.news-content {
  font-size: 1rem;
  color: #555;
}

.image-upload {
  margin-top: 10px;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 150px;
  height: 150px;
  margin: 0 auto;
  padding-left: 1rem;
}

.news-image {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 0.5rem;
}

.tag-overlay {
  position: absolute;
  top: 4px;
  left: 4px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 0.25rem;
  padding: 0.5rem;
}
</style>

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

                <div class="news-content" v-html="renderBlocks(newsItem.content)"></div>
              </div>

              <!-- Изображение новости справа -->
              <div class="image-container">
                <!-- Проверка на наличие изображения в контенте -->
                <img 
                  v-if="newsItem.image" 
                  class="news-image" 
                  :src="`http://localhost:8000/static/images/${newsItem.image}`" 
                  :alt="newsItem.header"
                />
                <div v-if="newsItem.image" class="tag-overlay">
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
import { PostService, Post } from "../api/serviceformedia";
import { initEditor } from "../editor.js/editor-init";

const post = ref<Post>({
  header: "",
  content: "",
  date_created: new Date(),
});

const visible = ref(false);
const editorContainer = ref<HTMLElement | null>(null);
let editorInstance: any = null;

const newsList = ref<Post[]>([]); // Список новостей
const postService = new PostService();

const renderBlocks = (content: string): string => {
  try {
    const parsedContent = JSON.parse(content);

    // Проверяем, что блоки есть и это массив
    if (parsedContent.blocks && Array.isArray(parsedContent.blocks)) {
      return parsedContent.blocks
        .map((block) => {
          if (block.type === "image" && block.data.file && block.data.file.url) {
            // Рендер блока изображения
            return `<img src="${block.data.file.url}" alt="image" style="max-width: 100%; margin-bottom: 10px;" />`;
          }
          // Можно добавить другие блоки по мере необходимости
          return "";
        })
        .join(""); // Склеиваем все блоки в строку
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

  try {
    const response = await fetch("http://localhost:8000/admin/media", {
      method: "POST",
      body: content,
    });

    if (response.ok) {
      console.log("Post added successfully");
      loadNews(); // Обновление списка новостей
    } else {
      console.error("Error adding post:", response.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
  }

  post.value = {
    header: "",
    content: "",
    date_created: new Date(),
  };

  editorInstance.clear();
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
  margin: 0;
  max-width: 50px;
  max-height: 50px;
}
img {
  width: 50px;        /* Устанавливаем ширину изображения */
  height: 50px;       /* Устанавливаем высоту изображения */
  object-fit: cover;  /* Изображение будет обрезано, чтобы заполнить контейнер */
  border-radius: 5px; /* Добавим скругление углов, если нужно */
}
.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50px;
  height: 50px;
  margin: 0 auto;
  padding-left: 1rem;
}

.news-image {
  width: 50px;  /* Устанавливаем ширину изображения 50px */
  height: 50px; /* Устанавливаем высоту изображения 50px */
  object-fit: cover; /* Изображение не будет искажаться, сохраняются пропорции */
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

@media (min-width: 768px) {
  .news-item {
    flex-direction: row;
    gap: 2rem;
  }

  .news-info {
    flex-grow: 1;
  }

  .image-container {
    max-width: 50px; /* Ограничиваем контейнер до 50px */
    padding-left: 1.5rem;
  }
}
</style>

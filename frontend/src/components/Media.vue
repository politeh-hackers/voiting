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
      class="dialog-main"
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
    <Dialog
      v-model:visible="visibledt"
      @show="initializeEditor"
      modal
      header="Добавить новость"
      :style="{ width: '60rem' }"
      class="dialog-edit"
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

        <Button icon="pi pi-check" @click="SaveEditedPost" />
      </div>
    </Dialog>

    <DataView
      :value="newsList"
      paginator
      :rows="5"
      dataKey="'id'"
      class="main-dataview"
    >
      <template #list="slotProps">
        <div class="news-container">
          <div
            v-for="newsItem in slotProps.items"
            :key="newsItem.id"
            class="news-item"
          >
            <div class="image-block">
              <img
                v-if="newsItem.main_photo"
                class="news-image"
                :src="`http://localhost:8000/static/images/${newsItem.main_photo}`"
                :alt="newsItem.header"
              />
            </div>
            <div class="title-block">
              <div class="news-title">{{ newsItem.header }}</div>
            </div>
            <div class="date-block">
              <span class="news-date">
                {{ new Date(newsItem.date_created).toLocaleDateString() }}
              </span>
            </div>
            <div class="action-buttons">
              <Button
                icon="pi pi-pencil"
                label="Редактировать"
                class="p-button-warning p-mr-2"
                @click="editPost(newsItem)"
              />
              <Button
                icon="pi pi-trash"
                label="Удалить"
                class="p-button-danger"
                @click="deletePost(newsItem.id)"
              />
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
const visibledt = ref(false);
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

const SaveEditedPost = async () => {
  if (!post.value.id) {
    console.error("Post ID is missing");
    return;
  }

  // Получаем обновленный контент из редактора
  post.value.content = await editorInstance
    .save()
    .then((data) => JSON.stringify(data));

  const postData = {
    content: post.value.content,
    header: post.value.header,
    summary: post.value.summary,
    main_photo: post.value.main_photo, // При необходимости отправьте изображение
  };

  try {
    // Отправка PATCH-запроса с JSON
    const response = await fetch(
      `http://localhost:8000/admin/media/${post.value.id}`,
      {
        method: "PATCH", // Используем PATCH для обновления
        headers: {
          "Content-Type": "application/json", // Указываем, что данные передаются в формате JSON
        },
        body: JSON.stringify(postData), // Преобразуем данные в JSON-строку
      }
    );

    if (response.ok) {
      console.log("Post edited successfully");
      loadNews(); // Обновление списка новостей
      post.value = {
        // Сбрасываем форму
        summary: "",
        main_photo: "",
        header: "",
        content: "",
        date_created: new Date(),
      };
      visibledt.value = false; // Закрытие диалога после сохранения изменений
    } else {
      const errorData = await response.json();
      console.error("Error updating post:", errorData);
    }
  } catch (error) {
    console.error("Error:", error);
  }
};

const renderBlocks = (content: string): string => {
  try {
    const parsedContent = JSON.parse(content);

    if (parsedContent.blocks && Array.isArray(parsedContent.blocks)) {
      return parsedContent.blocks
        .map((block) => {
          if (
            block.type === "image" &&
            block.data.file &&
            block.data.file.url
          ) {
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
  content.append("summary", post.value.summary);

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
      post.value.summary = "";
      visible.value = false; // Закрытие формы
    } else {
      console.error("Error adding post:", response.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
  }
};

// Редактирование новости
const editPost = (newsItem) => {
  post.value.id = newsItem.id;
  post.value.header = newsItem.header;
  post.value.summary = newsItem.summary;
  post.value.main_photo = newsItem.main_photo;
  post.value.content = newsItem.content;

  visibledt.value = true; // Открываем диалог

  setTimeout(() => {
    try {
      // Преобразуем строку в объект и передаем только блоки
      const editorData = {
        blocks: JSON.parse(newsItem.content).blocks,
      };

      if (editorInstance) {
        editorInstance.clear();
        editorInstance.render(editorData);
      } else {
        initializeEditor();
        editorInstance.render(editorData);
      }
    } catch (error) {
      console.error("Error rendering editor data:", error);
    }
  }, 100);
};

// Удаление новости
const deletePost = async (postId: string) => {
  try {
    const response = await fetch(
      `http://localhost:8000/admin/media/${postId}`,
      {
        method: "DELETE",
      }
    );
    deleteImage("http://localhost:8000/admin/media");
    if (response.ok) {
      console.log("Post deleted successfully");
      loadNews(); // Обновление списка новостей
    } else {
      console.error("Error deleting post:", response.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
  }
};
const deleteImage = (fileUrl: string) => {
  const imageName = fileUrl.split("/").pop();

  return fetch(`http://127.0.0.1:8000/admin/image/${imageName}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ file_url: fileUrl }),
  }).then((response) => {
    if (!response.ok) {
      alert("Ошибка при удалении изображения. Свяжитесь с администратором.");
    }
  });
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
.news-header {
  display: grid;
  grid-template-columns: 1fr 2fr 1fr 1fr; /* Оформляем как сетку с 4 колонками */
  gap: 20px;
  font-weight: bold;
  padding: 10px 0;
  border-bottom: 2px solid #e0e0e0;
}

.news-header .image-label,
.news-header .title-label,
.news-header .date-label,
.news-header .actions-label {
  text-align: center; /* Выравнивание по центру */
}

.news-container {
  display: flex;
  flex-direction: column;
}

.news-item {
  display: flex;
  align-items: center; /* Выравнивание по центру по вертикали */
  padding: 1.5rem;
  gap: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.image-block {
  flex: 0 0 auto; /* Не растягивать изображение */
  margin-right: 1rem;
  border-right: 1px solid #e0e0e0; /* Линия справа от изображения */
  padding-right: 1rem;
}

.title-block {
  flex: 1; /* Заголовок будет занимать доступное пространство */
  border-right: 1px solid #e0e0e0; /* Линия справа от заголовка */
  padding-right: 1rem;
}

.date-block {
  font-size: 0.875rem;
  color: #888;
  border-right: 1px solid #e0e0e0; /* Линия справа от даты */
  padding-right: 1rem;
}

.news-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-top: 0.5rem;
}

.news-date {
  font-size: 0.875rem;
  color: #888;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.news-image {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 0.5rem;
}

.image-upload {
  margin-top: 10px;
}

.tag-overlay {
  position: absolute;
  top: 4px;
  left: 4px;
  background: rgba(0, 0, 0, 0.7);
  border-radius: 0.25rem;
  padding: 0.5rem;
}

.image-label,
.title-label,
.date-label,
.actions-label {
  font-weight: bold;
  margin-bottom: 5px;
}
</style>

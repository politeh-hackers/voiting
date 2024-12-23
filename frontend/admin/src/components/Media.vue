<template>
  <div class="card flex flex-column">
    <Dialog
      v-model:visible="visible"
      @show="initializeEditor"
      @hide="handleDialogClose"
      
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
            :showUploadButton="false"
            :showCancelButton="false"
            @upload="onImageUpload"
            @remove="onImageRemove"
            chooseLabel="Выбрать изображение"
          >
            <template #content>
              <div class="custom-file-upload">
                <!-- Отображение выбранного изображения -->
                <img
                  v-if="post.main_photo"
                  :src="`http://localhost:8000/static/image/${post.main_photo}`"
                  alt="Preview"
                  class="image-preview"
                />
                <Button
                  class="p-button-danger"
                  icon="pi pi-times"
                  @click="onImageRemove"
                />
              </div>
            </template>
          </FileUpload>
        </div>

        <div ref="editorContainer" class="content-editor"></div>

        <div class="date__picker">
          <DatePicker v-model="post.date_created" dateFormat="" />
        </div>

        <Button icon="pi pi-check" @click="addPost" />
      </div>
    </Dialog>
    <Dialog
      v-model:visible="visibledt"
      @show="initializeEditor"
      modal
      header="Изменить новость"
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
          <label for="image-upload">Изменить изображение:</label>
          <FileUpload
            name="main_photo"
            :url="'http://localhost:8000/admin/image'"
            accept="image/*"
            :auto="true"
            :showUploadButton="false"
            :showCancelButton="false"
            @upload="onImageUpload"
            @remove="onImageRemove"
            chooseLabel="Выбрать изображение" 
          >
            <template #content>
              <div class="custom-file-upload">
                <!-- Отображение выбранного изображения -->
                <img
                  v-if="post.main_photo"
                  :src="`http://localhost:8000/static/image/${post.main_photo}`"
                  alt="Preview"
                  class="image-preview"
                />
                <Button
                  class="p-button-danger"
                  @click="onImageRemove"
                  icon="pi pi-times"
                />
              </div>
            </template>
          </FileUpload>
        </div>

        <div ref="editorContainer" class="content-editor"></div>

        <div class="date__picker">
          <DatePicker v-model="post.date_created" dateFormat="" />
        </div>

        <Button icon="pi pi-check" @click="SaveEditedPost" />
      </div>
    </Dialog>

    <DataView
      :value="filteredNewsList"
      paginator
      :rows="5"
      dataKey="'id'"
      class="main-dataview"
    >
      <template #header>
        <div class="header__content">
        <Button
          class="content__view"
          icon="pi pi-plus"
          @click="visible = true"
        />
        <Dropdown
          v-model="sortOrder"
          :options="sortOptions"
          optionLabel="label"
          optionValue="value"
          class="p-dropdown"
        /><InputText
          v-model="searchQuery"
          placeholder="Поиск по описанию"
          class="search-input"
        />
      </div>
      </template>
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
                :src="`http://localhost:8000/static/image/${newsItem.main_photo}`"
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
import { ref, onMounted, computed, watch } from "vue";
import InputText from "primevue/inputtext";
import DatePicker from "primevue/datepicker";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import DataView from "primevue/dataview";
import FileUpload from "primevue/fileupload";
import { PostService, Post } from "../api/serviceformedia";
import { initEditor } from "../editor.js/editor-init";
import Dropdown from "primevue/dropdown";

const post = ref<Post>({
  summary: "",
  main_photo: "",
  header: "",
  content: "",
  date_created: new Date(),
});

const sortOrder = ref("asc");
let previousPhoto = ""; //
const visible = ref(false);
const visibledt = ref(false);
const editorContainer = ref<HTMLElement | null>(null);
let editorInstance: any = null;
const newsList = ref<Post[]>([]);
const postService = new PostService();
const searchQuery = ref("");
const sortOptions = [
  { label: "По дате(по возрастанию)", value: "asc" },
  { label: "По дате(по убыванию)", value: "desc" },
];

// Вычисляемое свойство для фильтрации
const filteredNewsList = computed(() => {
  const filtered = newsList.value.filter(
    (newsItem) =>
      newsItem.summary
        .toLowerCase()
        .includes(searchQuery.value.toLowerCase()) ||
      newsItem.header.toLowerCase().includes(searchQuery.value.toLowerCase())
  );

  // Сортировка по дате
  return filtered.sort((a, b) => {
    const dateA = new Date(a.date_created).getTime();
    const dateB = new Date(b.date_created).getTime();
    return sortOrder.value === "asc" ? dateA - dateB : dateB - dateA;
  });
});
const toggleSortOrder = () => {
  sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
};
const onImageUpload = (event: any) => {
  const uploadedImage = event.files[0];
  if (uploadedImage) {
    post.value.main_photo = uploadedImage.name;
    
  }
};
const onImageRemove = (event: any) => {
  console.log("Изображение удалено:", event.file);

  if (post.value.main_photo) {
    deleteImage(`http://localhost:8000/static/image/${post.value.main_photo}`)
      .then(() => {
        post.value.main_photo = ""; // Очищаем ссылку на фото
      })
      .catch((error) => {
        console.error("Ошибка при удалении изображения с сервера:", error);
      });
  } else {
    // Если файл не загружен, просто сбрасываем его в состоянии
    post.value.main_photo = "";
  }
};
const handleDialogClose = () => {
  // Проверяем, что окно было закрыто через крестик и поле изображения не пустое
  if (!visible.value && post.value.main_photo) {
    deleteImage(`http://localhost:8000/static/image/${post.value.main_photo}`);
    post.value.main_photo = ""; // Очищаем ссылку на фото
  }
  if (editorInstance) {
  editorInstance.clear();
  console.log("pizda")
  }
};

const SaveEditedPost = async () => {
  if (!post.value.id) {
    console.error("Отсутствует ID поста");
    return;
  }

  post.value.content = await editorInstance
    .save()
    .then((data) => JSON.stringify(data));

  const postData = {
    content: post.value.content,
    header: post.value.header,
    summary: post.value.summary,
    main_photo: post.value.main_photo,
  };

  const formattedDate = post.value.date_created.toLocaleDateString("en-CA");

  try {
    const response = await fetch(
      `http://localhost:8000/media/${post.value.id}`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ...postData, date_created: formattedDate }),
      }
    );

    if (response.ok) {
      console.log("Пост успешно отредактирован");
      loadNews();
      post.value = {
        summary: "",
        main_photo: "",
        header: "",
        content: "",
        date_created: new Date(),
      };
      visibledt.value = false;
    } else {
      const errorData = await response.json();
      console.error("Ошибка при обновлении поста:", errorData);
    }
  } catch (error) {
    console.error("Ошибка:", error);
  }
};

const loadNews = async () => {
  try {
    const response = await fetch("http://localhost:8000/media/");
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

  // Преобразуем дату в формат 'YYYY-MM-DD'
  const formattedDate = post.value.date_created.toLocaleDateString("en-CA");

  content.append("content", post.value.content);
  content.append("header", post.value.header);
  content.append("summary", post.value.summary);
  content.append("date_created", formattedDate);

  if (post.value.main_photo) {
    content.append("main_photo", post.value.main_photo);
  }

  try {
    const response = await fetch("http://localhost:8000/media/", {
      method: "POST",
      body: content,
    });

    if (response.ok) {
      console.log("Пост успешно добавлен");
      loadNews();
      post.value.header = "";
      post.value.summary = "";
      post.value.main_photo = "";
      post.value.content = "";
      editorInstance = null
      visible.value = false;
      
    } else {
      console.error("Ошибка при добавлении поста:", response.statusText);
    }
  } catch (error) {
    console.error("Ошибка:", error);
  }
};

// Редактирование новости
const editPost = (newsItem) => {
  post.value.id = newsItem.id;
  post.value.header = newsItem.header;
  post.value.summary = newsItem.summary;
  previousPhoto = newsItem.main_photo;
  post.value.main_photo = newsItem.main_photo;
  post.value.content = newsItem.content;
  post.value.date_created = newsItem.date_created;

  visibledt.value = true;

  setTimeout(() => {
    try {
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
      `http://localhost:8000/media/${postId}`,
      {
        method: "DELETE",
      }
    );
    deleteImage("http://localhost:8000/media");

    if (response.ok) {
      console.log("Post deleted successfully");
      loadNews();
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
  loadNews();
});
</script>
  
<style scoped lang="scss">

input {
  width: 100%; /* Ширина инпутов и текстовых полей */}



.content__main{
  display: flex;
  flex-direction: column;
  gap: 1.5rem; 
}
// .news-header {
//   display: grid;
//   grid-template-columns: 1fr 2fr 1fr 1fr;
//   gap: 20px;
//   font-weight: bold;
//   padding: 10px 0;
//   border-bottom: 2px solid #e0e0e0;
// }
.image-preview {
  max-width: 150px;
  max-height: 150px;
  object-fit: cover;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.news-header .image-label,
.news-header .title-label,
.news-header .date-label,
.news-header .actions-label {
  text-align: center;
}

.news-container {
  display: flex;
  flex-direction: column;
}

.news-item {
  display: flex;
  align-items: center;
  padding: 1.5rem;
  gap: 1rem;
  border-bottom: 1px solid #e0e0e0;
}

.image-block {
  flex: 0 0 auto;
  margin-right: 1rem;
  border-right: 1px solid #e0e0e0;
  padding-right: 1rem;
}

.title-block {
  flex: 1;
  border-right: 1px solid #e0e0e0;
  padding-right: 1rem;
}

.date-block {
  font-size: 0.875rem;
  color: #888;
  border-right: 1px solid #e0e0e0;
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
.content-editor{ 
}
.search-input {
}
.p-dropdown{
  align-items: center;
}
.header__content {
  display: flex;
  flex-direction: row;
  gap: 3px;
  height: 30px;
}
</style>
  
<template>
  <Dialog
    v-model:visible="visibledt"
    modal
    header="Обращение"
    :style="{ width: '60rem' }"
    class="dialog-edit"
  >
    <div class="content__main">
      <div class="components">
        <div class="category">
          <Select
            disabled
            v-model="selectedCategory"
            :options="items"
            optionLabel="name"
            placeholder="Select a Category"
          />
        </div>
        <div class="name">
          <InputText
            disabled
            v-model="post.first_name"
            placeholder="Имя"
            class="header__input"
          />
        </div>
        <div class="surname">
          <InputText
            disabled
            v-model="post.last_name"
            placeholder="Фамилия"
            class="summary_input"
          />
        </div>

        <div class="second_name">
          <InputText
            disabled
            v-model="post.patronymic"
            placeholder="Отчество"
            class="summary_input"
          />
        </div>

        <div class="flex-auto">
          <label for="phone" class="">Номер телефона</label>
          <InputText
            id="phone"
            disabled
            v-model="post.phone"
            placeholder="Номер телефона"
            fluid
          />
        </div>
        <div class="date_picker">
          <DatePicker disabled v-model="post.date" dateFormat="" />
        </div>
        <FloatLabel variant="on">
          <Textarea
            id="over_label"
            v-model="post.text"
            rows="5"
            cols="30"
            style="resize: none"
          />
          <label for="on_label">Текст обращения</label>
        </FloatLabel>
        <label for="image-upload">Просмотр изображений</label>
        <Image
          alt="main_photo"
          src="'http://localhost:8000/appeals/image'"
          width="250"
          preview
        />
        <div class="card flex flex-wrap justify-center gap-4">
          <Select
            v-model="statusitems"
            :options="status"
            optionLabel="name"
            placeholder="Select a Status"
          />
        </div>
        <div class="card flex flex-wrap justify-center gap-4">
          <div class="flex items-center gap-2">
            <Checkbox
              v-model="post.on_website"
              inputId="CheckWorked"
              name="on_website"
              value="OnWebsite"
            />
            <label for="CheckWorked"> На сайте </label>
          </div>
        </div>
        <FloatLabel variant="on">
          <Textarea
            id="over_label"
            v-model="post.official_response"
            rows="5"
            cols="30"
            style="resize: none"
          />
          <label for="on_label">Оффициальный ответ</label>
        </FloatLabel>
      </div>
    </div>
  </Dialog>
  <DataView
    :value="NewList"
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
            <div class="news-title">{{ newsItem.last_name }}</div>
          </div>
          <div class="date-block">
            <span class="news-date">
              {{ new Date(newsItem.date).toLocaleDateString() }}
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
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from "vue";
import InputText from "primevue/inputtext";
import DatePicker from "primevue/datepicker";
import Button from "primevue/button";
import Dialog from "primevue/dialog";
import DataView from "primevue/dataview";
import FileUpload from "primevue/fileupload";
import { PostService, Post } from "../api/serviceforappeals";
import Dropdown from "primevue/dropdown";
import Textarea from "primevue/textarea";
import Select from "primevue/select";
import InputMask from "primevue/inputmask";
import Checkbox from "primevue/checkbox";
import Image from "primevue/image";
import FloatLabel from "primevue/floatlabel";
import { getToken } from "../utils/auth";
const checked = ref(false);
const phone_number = ref("");
const selectedCategory = ref();
const post = ref<Post>({
  category: "",
  map_point: "",
  first_name: "",
  last_name: "",
  patronymic: "",
  phone: "",
  photos: "",
  text: "",
  on_website: false,
  date: new Date(),
  official_response: "",
});
const token = getToken()

const status = ref([
  { name: "Принято в работу", code: "Accepted" },
  { name: "Отклонено", code: "Abort" },
  { name: "Исполнено", code: "Success" },
]);
const statusitems = ref();
const visibledt = ref(false);
const NewList = ref<Post[]>([]);
const items = ref();
const loadAppeals = async () => {
  try {
    const response = await fetch("http://localhost:8000/appeals/",{
      method: "GET",
      headers:{
         'Authorization': `${token}`
      }
    });
    if (response.ok) {
      NewList.value = await response.json();
      console.log(NewList.value);
    } else {
      console.error("Failed to load news:", response.statusText);
    }
  } catch (error) {
    console.error("Error loading news:", error);
  }
};

const loadCategories = async () => {
  const response = await fetch("http://localhost:8000/category/",{
    headers:{
         'Authorization': `${token}`
    }
  });
  items.value = await response.json();
};

const editPost = (newsItem) => {
  post.value.id = newsItem.id;
  post.value.text = newsItem.text;
  post.value.map_point = newsItem.map_point;
  post.value.phone = newsItem.phone
  post.value.photos = newsItem.photos;
  post.value.first_name = newsItem.first_name;
  post.value.date = newsItem.date;
  post.value.last_name = newsItem.last_name;
  post.value.patronymic = newsItem.patronymic;
  visibledt.value = true;
};
onMounted(() => {
  loadAppeals();
  loadCategories();
});
</script>

<style scoped lang="scss">
.components {
  display: flex;
  flex-direction: column;
  gap: 1.5rem; /* Добавляем гэпы между всеми компонентами */}
.card.flex {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem; /* Добавляем гэпы в карточках */}
.input {
  margin-bottom: 1rem; /* Отступы между инпутами */}
textarea, input {
  width: 100%; /* Ширина инпутов и текстовых полей */}
.action-buttons {
  display: flex;
  gap: 10px;
  justify-content: center;
}
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
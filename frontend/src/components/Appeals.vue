<template>
    <Dialog
      v-model:visible="visibledt"
      
      modal
      header="Изменить новость"
      :style="{ width: '60rem' }"
      class="dialog-edit"
    >
      <div class="content__main">
        <div class = "category">
            <Select v-model = "selectedCategory" :options="items" optionLabel="name" placeholder="Select a Category"/>
        </div>
        <div class="name">
          <InputText
            v-model="post.first_name"
            placeholder="Имя"
            class="header__input"
          />
        </div>
        <div class="surname">
          <InputText
            v-model="post.last_name"
            placeholder="Фамилия"
            class="summary_input"
          />
        </div>
        <div class="second_name">
          <InputText
            v-model="post.patronymic"
            placeholder="Отчество"
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
            @upload="onImageUpload"
            chooseLabel="Выбрать изображение"
          />
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
import Textarea from 'primevue/textarea';
import Select from 'primevue/select';


const selectedCategory = ref();
const post = ref<Post>({
  category: "",
  map_point:"",
  first_name:"",
  last_name:"",
  patronymic:"",
  phone_number:"",
  photos: "",
  appeal_text: "",
  date_created: new Date(),
  official_response:""
  
});
const visibledt = ref(false)
const NewList = ref<Post[]>([]);
const items = ref()
const loadAppeals = async () => {
  try {
    const response = await fetch("http://localhost:8000/admin/appeal");
    if (response.ok) {
      NewList.value = await response.json();
      console.log(NewList.value)
    } else {
      console.error("Failed to load news:", response.statusText);
    }
  } catch (error) {
    console.error("Error loading news:", error);
  }
};

const loadCategories = async() =>{
    const response = await fetch("http://localhost:8000/admin/category")
    items.value = await response.json()
}

const editPost = (newsItem) => {
  post.value.id = newsItem.id;
  post.value.appeal_text = newsItem.appeal_text;
  post.value.map_point = newsItem.map_point;
  post.value.photos = newsItem.photos;
  post.value.first_name = newsItem.first_name;
  post.value.date_created = newsItem.date_created
  post.value.last_name = newsItem.last_name
  post.value.patronymic = newsItem.patronymic


  visibledt.value = true; 

  
};
onMounted(() => {
  loadAppeals();
  loadCategories();
});
</script>

<style lang="scss">
</style>
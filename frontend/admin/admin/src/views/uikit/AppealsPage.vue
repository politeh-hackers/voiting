<template>
  <div class="appeals-page">
    <h1 class="text-4xl font-bold mb-4">Обращения</h1>
    <Sidebar
      v-model:visible="visibledt"
      position="right"
      :style="{ width: '60rem' }"
      class="sidebar-edit"
    >
      <template #header>
        <h2>Обращение</h2>
      </template>
      <div class="flex flex-col gap-6">
        <div class="flex flex-col gap-6">
  
          <div class="flex flex-col">
            <label class="mb-2">Категория обращения</label>
            <Select v-model="selectedCategory" :options="items" optionLabel="name" :placeholder="post.category" class="w-full" />
          </div>
          <div class="flex flex-col">
            <label class="mb-2">Имя</label>
            <InputText disabled v-model="post.first_name" placeholder="Введите имя" class="w-full" />
          </div>
          <div class="flex flex-col">
            <label class="mb-2">Фамилия</label>
            <InputText disabled v-model="post.last_name" placeholder="Введите фамилию" class="w-full" />
          </div>
  
          <div class="flex flex-col">
            <label class="mb-2">Отчество</label>
            <InputText disabled v-model="post.patronymic" placeholder="Введите отчество" class="w-full" />
          </div>
  
          <div class="flex flex-col">
            <label class="mb-2">Номер телефона</label>
            <InputText id="phone" disabled v-model="post.phone" placeholder="Введите номер телефона" class="w-full" />
          </div>
          <div class="flex flex-col">
            <label class="mb-2">Дата обращения</label>
            <DatePicker disabled v-model="post.date" dateFormat="" class="w-full" />
          </div>
          <div class="flex flex-col">
            <label class="mb-2">Текст обращения</label>
            <Textarea v-model="post.text" rows="5" cols="30" class="resize-none w-full" />
          </div>
          <div class="flex flex-col">
            <label class="mb-2">Прикрепленные изображения</label>
            <div class="flex flex-wrap gap-4">
              <Image v-for="(photo, index) in post.photos" :key="index" :src="photo" width="250" preview />
            </div>
          </div>
          <div class="flex flex-col">
            <label class="mb-2">Статус обращения</label>
            <Select v-model="post.status" :options="status" optionLabel="name" option-value="name"
              placeholder="Выберите статус" class="w-full" />
          </div>
          <div class="flex items-center gap-2">
            <Checkbox v-model="post.on_website" inputId="CheckWorked" name="on_website" binary />
            <label for="CheckWorked">Отображать на сайте</label>
          </div>
          <div class="flex flex-col">
            <label class="mb-2">Официальный ответ</label>
            <Textarea v-model="post.official_response" rows="5" cols="30" class="resize-none w-full" />
          </div>
          <div class="flex flex-col sm:flex-row gap-4 mt-4">
            <Button 
              icon="pi pi-check" 
              label="Сохранить"
              @click="SavePost()" 
              class="p-button-warning w-full sm:w-[200px]" 
            />
            <Button 
              icon="pi pi-times" 
              label="Отмена"
              @click="visibledt = false" 
              class="p-button-secondary w-full sm:w-[200px]" 
            />
          </div>
        </div>
      </div>
    </Sidebar>
    <DataView
      :value="filteredAppeals"
      paginator
      :rows="10"
      dataKey="'id'"
      class="w-full"
    >
      <template #header>
        <div class="flex flex-col sm:flex-row w-full gap-4">
          <div class="flex flex-col sm:flex-row flex-1 gap-4">
            <Dropdown
              v-model="sortField"
              :options="sortOptions"
              optionLabel="label"
              optionValue="value"
              placeholder="Сортировать по"
              class="w-full sm:w-[200px]"
            />
            <Dropdown
              v-model="selectedStatus"
              :options="status"
              optionLabel="name"
              placeholder="Фильтр по статусу"
              class="w-full sm:w-[200px]"
            />
            <InputText
              v-model="searchQuery"
              placeholder="Поиск по тексту или категории"
              class="w-full"
            />
          </div>
        </div>
      </template>
      <template #list="slotProps">
        <div class="flex flex-col w-full">
          <div
            v-for="newsItem in slotProps.items"
            :key="newsItem.id"
            class="flex flex-col sm:flex-row items-start sm:items-center p-4 sm:p-6 gap-4 border-b border-gray-200"
          >
            <div class="w-full sm:w-auto sm:flex-none sm:mr-4 sm:border-r sm:border-gray-200 sm:pr-4">
              <img
                v-if="newsItem.main_photo"
                class="w-full sm:w-[100px] h-[100px] object-cover rounded-lg"
                :src="`http://localhost:8000/static/images/${newsItem.main_photo}`"
                :alt="newsItem.header"
              />
            </div>
            <div class="w-full sm:flex-1 sm:border-r sm:border-gray-200 sm:pr-4">
              <div class="text-xl font-semibold">{{ newsItem.last_name }}</div>
            </div>
            <div class="w-full sm:w-auto text-sm text-gray-500 sm:border-r sm:border-gray-200 sm:pr-4">
              <span>
                {{ new Date(newsItem.date).toLocaleDateString() }}
              </span>
            </div>
            <div class="flex flex-col w-full sm:w-auto gap-2.5">
              <Button
                icon="pi pi-pencil"
                label="Редактировать"
                class="p-button-warning w-full sm:w-[150px]"
                @click="editPost(newsItem)"
              />
              <Button
                icon="pi pi-trash"
                label="Удалить"
                class="p-button-danger w-full sm:w-[150px]"
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
import { useRouter } from "vue-router";
import { ref, onMounted, computed, watch } from "vue";
import InputText from "primevue/inputtext";
import DatePicker from "primevue/datepicker";
import Button from "primevue/button";
import Sidebar from "primevue/sidebar";
import DataView from "primevue/dataview";
import FileUpload from "primevue/fileupload";
import { PostService, Post } from "../../api/serviceforappeals";
import Dropdown from "primevue/dropdown";
import Textarea from "primevue/textarea";
import Select from "primevue/select";
import InputMask from "primevue/inputmask";
import Checkbox from "primevue/checkbox";
import Image from "primevue/image";
import FloatLabel from "primevue/floatlabel";
import { getToken, isAuthenticated } from "../../utils/auth";
import { title } from "process";
  
const checked = ref(false);
const phone_number = ref("");
const selectedCategory = ref();
const post = ref<Post>({
  h1: "",
  title: "",
  description: "",
  category: "",
  map_point: "",
  first_name: "",
  last_name: "",
  patronymic: "",
  phone: "",
  photos: "",
  status: "",
  text: "",
  on_website: false,
  date: new Date(),
  official_response: "",
  date_responce: new Date(),
});
const token = getToken()
const router = useRouter()
const status = ref([
  { name: "Без статуса", code: "None"},
  { name: "Принято в работу", code: "Accepted" },
  { name: "Отклонено", code: "Abort" },
  { name: "Исполнено", code: "Success" },
]);
const statusitems = ref();
const visibledt = ref(false);
const NewList = ref<Post[]>([]);
const items = ref();
const sortField = ref("date");
const searchQuery = ref("");
const selectedStatus = ref(null);
const sortOptions = [
  { label: "По дате (новые)", value: "date_desc" },
  { label: "По дате (старые)", value: "date_asc" },
];

const loadAppeals = async () => {
  try {
    const response = await fetch("http://localhost:8000/appeals/appeals", {
      method: "GET",
      headers: {
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
  const response = await fetch("http://localhost:8000/category/", {
    headers: {
      'Authorization': `${token}`
    }
  });
  items.value = await response.json();
};
const deletePost = async (postId: string) => {
  if (!isAuthenticated(token)) {
    router.push({ name: 'Home' });
    return;
  }
  try {
    const response = await fetch(
      `http://localhost:8000/appeals/${postId}`,
      {
        method: "DELETE",
        headers: {
          'Authorization': `${token}`
        }
      }
    );
    if (response.ok) {
      console.log("Post deleted successfully");
      loadAppeals();
    } else {
      console.error("Error deleting post:", response.statusText);
    }
  } catch (error) {
    console.error("Error:", error);
  }
};
const editPost = (newsItem) => {
  post.value.category = newsItem.category
  post.value.h1 = newsItem.h1
  post.value.title = newsItem.title
  post.value.description = newsItem.description
  post.value.id = newsItem.id;
  post.value.text = newsItem.text;
  post.value.map_point = newsItem.map_point;
  post.value.phone = newsItem.phone
  post.value.photos = newsItem.photos;
  post.value.first_name = newsItem.first_name;
  post.value.date = newsItem.date;
  post.value.status = newsItem.status;
  post.value.last_name = newsItem.last_name;
  post.value.patronymic = newsItem.patronymic;
  post.value.official_response = newsItem.official_response;
  post.value.on_website = newsItem.on_website
  post.value.date_responce = newsItem.date_responce
  visibledt.value = true;
};
  
const SavePost = async () => {
  if (!isAuthenticated(token)) {
    router.push({ name: 'Home' });
    return;
  }
  console.log(post.value);
  const postData = {
    category: post.value.category,
    h1: post.value.h1,
    title: post.value.title,
    description: post.value.description,
    text: post.value.text,
    on_website: post.value.on_website,
    status: post.value.status,
    official_response: post.value.official_response,
    date_responce: post.value.date_responce ? new Date(post.value.date_responce).toISOString().split('T')[0] : null
  };
  try {
    console.log(postData)
    const response = await fetch(
      `http://localhost:8000/appeals/${post.value.id}`,
      {
        method: "PATCH",
        headers: {
          'Authorization': `${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify(postData),
      }
    );

    if (response.ok) {
      console.log("Пост успешно отредактирован");
      loadAppeals();
      post.value = {
        h1: "",
        title: "",
        description: "",
        category: "",
        map_point: "",
        first_name: "",
        last_name: "",
        patronymic: "",
        phone: "",
        photos: "",
        text: "",
        status: "",
        on_website: false,
        date: new Date(),
        official_response: "",
        date_responce: new Date(),
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
  
// Вычисляемое свойство для фильтрации и сортировки
const filteredAppeals = computed(() => {
  let filtered = [...NewList.value];

  // Фильтрация по поисковому запросу
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (appeal) =>
        appeal.text?.toLowerCase().includes(query) ||
        appeal.category?.toLowerCase().includes(query)
    );
  }

  // Фильтрация по статусу
  if (selectedStatus.value) {
    filtered = filtered.filter(
      (appeal) => appeal.status === selectedStatus.value.name
    );
  }

  // Сортировка
  filtered.sort((a, b) => {
    switch (sortField.value) {
      case "date_desc":
        return new Date(b.date).getTime() - new Date(a.date).getTime();
      case "date_asc":
        return new Date(a.date).getTime() - new Date(b.date).getTime();
      case "status":
        return (a.status || "").localeCompare(b.status || "");
      default:
        return new Date(b.date).getTime() - new Date(a.date).getTime();
    }
  });

  return filtered;
});
  
onMounted(() => {
  loadAppeals();
  loadCategories();
});
</script>
  
<style scoped>
.appeals-page {
  @apply p-4;
}

.sidebar-main,
.sidebar-edit {
  @apply w-full;
}

@media (min-width: 640px) {
  .sidebar-main,
  .sidebar-edit {
    width: 60rem !important;
  }
}

:deep(.p-sidebar-content) {
  @apply p-4 sm:p-8;
}

:deep(.p-fileupload-content) {
  @apply p-4;
}

:deep(.p-datepicker) {
  @apply w-full;
}

:deep(.p-dropdown) {
  @apply w-full sm:w-auto;
}

:deep(.p-button) {
  @apply justify-center;
}

:deep(.p-inputtext) {
  @apply w-full;
}

:deep(.p-checkbox) {
  @apply mr-2;
}

:deep(.p-textarea) {
  @apply w-full;
}
</style>
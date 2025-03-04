<script setup lang="ts">
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import { PostService, Post } from "../../api/service";
import { onMounted } from "vue";
import InputText from "primevue/inputtext";
import { Button } from "primevue";
import { ref } from "vue";
import Drawer from "primevue/drawer";
import { useRouter } from "vue-router";
import { getToken, isAuthenticated } from "../../utils/auth"; // Импортируем утилиту для проверки токена
import Dropdown from "primevue/dropdown";

const router = useRouter();
const postService = new PostService();
const prefix = "category";

const posts = ref<Post[]>([]);
const post = ref<Post>({ name: "" });
const editingPostId = ref<string | null>(null);
const editingPostName = ref<string>(""); 
const visible = ref(false); 
const visibleEdit = ref(false); // Добавляем новую переменную для окна редактирования
const token = getToken()
const sortOrder = ref<{ label: string; value: string } | null>(null);
const sortOptions = [
  { label: 'По возрастанию', value: 'asc' },
  { label: 'По убыванию', value: 'desc' },
];
const searchQuery = ref("");

const UpdateTable = async () => {
  if (!isAuthenticated(token)) {
    router.push({ name: 'Login' }); // Перенаправляем на страницу входа, если пользователь не авторизован
    return;
  }

  const results = await postService.getAll(prefix);
  posts.value = results;
};

onMounted(UpdateTable);

const addPost = async () => {
  if (!isAuthenticated(token)) {
    router.push({ name: 'Home' });
    console.log("pizda")
    return;
  }

  await postService.create(post.value, prefix);
  post.value.name = "";
  visible.value = false; // Закрываем сайдбар после добавления
  await UpdateTable();
};

const deletePost = async (id: string) => {
  if (!isAuthenticated(token)) {
    router.push({ name: 'Home' });
    return;
  }

  await postService.delete(prefix, id);
  posts.value = posts.value.filter((post) => post.id !== id);
  await UpdateTable();
};

const startEditing = (id: string, name: string) => {
  if (!isAuthenticated(token)) {
    router.push({ name: 'Home' });
    return;
  }

  editingPostId.value = id; 
  editingPostName.value = name; 
  visibleEdit.value = true; // Используем новую переменную
};

const saveEditedPost = async () => {
  if (!isAuthenticated(token)) {
    router.push({ name: 'Home' });
    return;
  }

  if (editingPostId.value) {
    await postService.patch(prefix, editingPostId.value ,{
      name: editingPostName.value,
    });
    editingPostId.value = null; 
    editingPostName.value = ""; 
    visibleEdit.value = false; // Используем новую переменную
    await UpdateTable();
  }
};
</script>

<template>
  <div class="category-page">
    <h1 class="text-2xl font-bold mb-4">Категории</h1>
    <DataTable 
      :value="posts" 
      class="main-datatable"
      :paginator="true"
      :rows="10"
      :rowsPerPageOptions="[10, 20, 30]"
    >
      <Column field="name">
        <template #body="slotProps">
          {{ slotProps.data.name }}
        </template>
      </Column>
      
      <Column>
        <template #header>
          <div class="flex flex-col sm:flex-row w-full gap-4">
            <div class="flex flex-1">
              <InputText
                v-model="searchQuery"
                placeholder="Поиск"
                class="w-full"
              />
            </div>
            <Button
              icon="pi pi-plus"
              label="Добавить"
              class="p-button-warning w-full sm:w-auto"
              @click="visible = true"
            />
          </div>
        </template>
        <template #body="slotProps">
          <div class="flex flex-col gap-4">
            <Button
              icon="pi pi-pencil"
              label="Изменить"
              class="p-button-warning w-full sm:w-[150px]"
              @click="startEditing(slotProps.data.id, slotProps.data.name)"
            />
            <Button
              icon="pi pi-trash"
              label="Удалить"
              class="p-button-danger w-full sm:w-[150px]"
              @click="deletePost(slotProps.data.id)"
            />
          </div>
        </template>
      </Column>
    </DataTable>
    
    <Drawer v-model:visible="visibleEdit" header="Редактировать категорию" position="right" class="sidebar-edit">
      <div class="p-4">
        <h3 class="text-lg font-semibold mb-4">Редактирование</h3>
        <div class="flex flex-col gap-4">
          <div class="flex flex-col">
            <label class="mb-2">Название категории</label>
            <InputText
              v-model="editingPostName"
              placeholder="Введите новое имя категории"
              class="w-full"
            />
          </div>
          <div class="flex flex-col sm:flex-row gap-4">
            <Button 
              icon="pi pi-check"
              label="Сохранить" 
              class="p-button-warning w-full sm:w-[200px]" 
              @click="saveEditedPost" 
            />
            <Button 
              icon="pi pi-times"
              label="Отмена" 
              class="p-button-secondary w-full sm:w-[200px]" 
              @click="visibleEdit = false" 
            />
          </div>
        </div>
      </div>
    </Drawer>

    <Drawer v-model:visible="visible" header="Добавить категорию" position="right" class="sidebar-main">
      <div class="p-4">
        <h3 class="text-lg font-semibold mb-4">Добавление</h3>
        <div class="flex flex-col gap-4">
          <div class="flex flex-col">
            <label class="mb-2">Название категории</label>
            <InputText
              v-model="post.name"
              placeholder="Введите имя категории"
              class="w-full"
            />
          </div>
          <div class="flex flex-col sm:flex-row gap-4">
            <Button 
              icon="pi pi-check"
              label="Сохранить" 
              class="p-button-warning w-full sm:w-[200px]" 
              @click="addPost" 
            />
            <Button 
              icon="pi pi-times"
              label="Отмена" 
              class="p-button-secondary w-full sm:w-[200px]" 
              @click="visible = false" 
            />
          </div>
        </div>
      </div>
    </Drawer>
  </div>
</template>

<style scoped>
.category-page {
  @apply p-4;
}

.main-datatable {
  @apply w-full;
}

.sidebar-main,
.sidebar-edit {
  @apply w-full;
}

@media (min-width: 640px) {
  .sidebar-main,
  .sidebar-edit {
    width: 30rem !important;
  }
}

:deep(.p-sidebar-content) {
  @apply p-4 sm:p-8;
}

:deep(.p-datatable) {
  @apply overflow-x-auto;
}

:deep(.p-column-header-content) {
  @apply w-full;
}

:deep(.p-inputtext) {
  @apply w-full;
}

:deep(.p-button) {
  @apply justify-center;
}

:deep(.p-paginator) {
  @apply flex-wrap justify-center;
}

@media (max-width: 640px) {
  :deep(.p-datatable-wrapper) {
    @apply overflow-x-auto;
  }
  
  :deep(.p-datatable table) {
    @apply w-full;
  }
  
  :deep(.p-column-title) {
    @apply whitespace-normal;
  }
}
</style>

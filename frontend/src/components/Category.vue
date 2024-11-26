<script setup lang="ts">
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import { PostService, Post } from "../api/service";
import { onMounted } from "vue";
import InputText from "primevue/inputtext";
import { Button } from "primevue";
import { ref } from "vue";
import Drawer from "primevue/drawer";

const postService = new PostService();
const baseAdmin = "admin";
const prefix = "category";

const posts = ref<Post[]>([]);
const post = ref<Post>({ name: "" });
const editingPostId = ref<string | null>(null);
const editingPostName = ref<string>(""); // Храним значение редактируемого имени
const visible = ref(false); // Управляет видимостью Drawer

const UpdateTable = async () => {
  const results = await postService.getAll(prefix, baseAdmin);
  posts.value = results;
};

onMounted(UpdateTable);

const addPost = async () => {
  await postService.create(post.value, prefix, baseAdmin);
  post.value.name = "";
  await UpdateTable();
};

const deletePost = async (id: string) => {
  await postService.delete(prefix, id, baseAdmin);
  posts.value = posts.value.filter((post) => post.id !== id);
  await UpdateTable();
};

const startEditing = (id: string, name: string) => {
  editingPostId.value = id; // Устанавливаем ID редактируемого поста
  editingPostName.value = name; // Копируем текущее имя в редактируемое поле
  visible.value = true; // Открываем Drawer
};

const saveEditedPost = async () => {
  if (editingPostId.value) {
    await postService.patch(prefix, editingPostId.value, baseAdmin, {
      name: editingPostName.value,
    });
    editingPostId.value = null; // Сбрасываем режим редактирования
    editingPostName.value = ""; // Очищаем редактируемое имя
    visible.value = false; // Закрываем Drawer
    await UpdateTable();
  }
};
</script>


<template>
  <div>
    <h1>Категории</h1>
    <DataTable :value="posts" tableStyle="min-width: 50rem">
      <!-- Колонка с именем категории -->
      <Column field="name" header="Имя категории">
        <template #body="slotProps">
          {{ slotProps.data.name }}
        </template>
      </Column>
      
      <!-- Колонка с действиями -->
      <Column header="Действия">
        <template #body="slotProps">
          <!-- Кнопка для редактирования -->
          <Button
            label="Изменить"
            class="p-button-warning"
            @click="startEditing(slotProps.data.id, slotProps.data.name)"
          />
          
          <!-- Кнопка для удаления -->
          <Button
            label="Удалить"
            class="p-button-danger"
            @click="deletePost(slotProps.data.id)"
          />
        </template>
      </Column>
    </DataTable>
    
    <!-- Drawer для редактирования -->
    <Drawer v-model:visible="visible" header="Редактировать категорию" position="right" style="width: 30vw;">
      <div>
        <h3>Редактирование</h3>
        <InputText
          v-model="editingPostName"
          placeholder="Введите новое имя категории"
          class="p-mb-3"
        />
        <Button label="Сохранить" class="p-button-success" @click="saveEditedPost" />
        <Button label="Отмена" class="p-button-secondary" @click="visible = false" />
      </div>
    </Drawer>

    <!-- Добавление новой категории -->
    <div>
      <InputText
        class="name_post"
        placeholder="Имя категории"
        v-model="post.name"
      />
      <Button @click="addPost">Добавить категорию</Button>
    </div>
  </div>
</template>



<style scoped>
</style>




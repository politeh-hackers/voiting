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

const router = useRouter();
const postService = new PostService();
const prefix = "category";

const posts = ref<Post[]>([]);
const post = ref<Post>({ name: "" });
const editingPostId = ref<string | null>(null);
const editingPostName = ref<string>(""); 
const visible = ref(false); 
const token = getToken()
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
  visible.value = true; 
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
    visible.value = false; 
    await UpdateTable();
  }
};
</script>

<template>
  <div>
    <h1>Категории</h1>
    <DataTable :value="posts" tableStyle="min-width: 50rem">
      <Column field="name" header="Имя категории">
        <template #body="slotProps">
          {{ slotProps.data.name }}
        </template>
      </Column>
      
      <Column header="Действия">
        <template #body="slotProps">
          <Button
            label="Изменить"
            class="p-button-warning"
            @click="startEditing(slotProps.data.id, slotProps.data.name)"
          />
          
          <Button
            label="Удалить"
            class="p-button-danger"
            @click="deletePost(slotProps.data.id)"
          />
        </template>
      </Column>
    </DataTable>
    
    <Drawer v-model:visible="visible" header="Редактировать категорию" position="right" style="width: 30vw;">
      <div>
        <h3>Редактирование</h3>
        <InputText
          v-model="editingPostName"
          placeholder="Введите новое имя категории"
          class="p-mb-3"
        />
        <Button label="Сохранить" @click="saveEditedPost" />
        <Button label="Отмена" class="p-button-secondary" @click="visible = false" />
      </div>
    </Drawer>

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

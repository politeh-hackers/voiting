<template>
  <div class="actual-page">
    <h1>Актуальное</h1>
    
      <Sidebar
        v-model:visible="visible"
        @show="initializeEditor"
        @hide="handleDialogClose"
        position="right"
        :style="{ width: '60rem' }"
        class="sidebar-main"
      >
        <template #header>
          <h2>Добавить новость</h2>
        </template>
        <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50 z-50">
          <i class="pi pi-spin pi-spinner text-4xl text-white"></i>
        </div>
        <div class="flex flex-col gap-6">
            <div class="flex flex-col">
              <label class="mb-2">URL страницы (slug)</label>
              <InputText
                v-model="post.slug"
                placeholder="Введите URL страницы"
                class="w-full"
              />
              
            </div>
            <div class="flex flex-col">
              <label class="mb-2">H1 заголовок</label>
              <InputText
                v-model="post.h1"
                placeholder="Введите H1 заголовок"
                class="w-full"
              />
            </div>
            <div class="flex flex-col">
              <label class="mb-2">Title страницы</label>
              <InputText
                v-model="post.title"
                placeholder="Введите title страницы"
                class="w-full"
              />
            </div>
            <div class="flex flex-col">
              <label class="mb-2">Meta description</label>
              <InputText
                v-model="post.description"
                placeholder="Введите meta description"
                class="w-full"
              />
            </div>
            <div class="flex flex-col">
              <label class="mb-2">Заголовок новости</label>
              <InputText
                v-model="post.header"
                placeholder="Введите заголовок новости"
                class="w-full"
              />
              <span v-if="post.header && post.header.length < 4" class="text-red-500 text-sm">
              Заголовок должен содержать минимум 4 символа
            </span>
            </div>
            <div class="flex flex-col">
              <label class="mb-2">Краткое описание</label>
              <InputText
                v-model="post.summary"
                placeholder="Введите краткое описание"
                class="w-full"
              />
              <span v-if="post.summary && post.summary.length < 4" class="text-red-500 text-sm">
              Краткое описание должно содержать минимум 4 символа
            </span>
            </div>
            <div class="flex flex-col">
              <label class="mb-2">Изображение новости</label>
              <FileUpload
                name="main_photo"
                :url="'http://localhost:8000/admin/image'"
                accept="image/*"
                :auto="true"
                :showUploadButton="false"
                :showCancelButton="false"
                @upload="onImageUpload"
                @remove="onImageRemove"
                :before-upload="uploadHeaders"
                chooseLabel="Выбрать изображение"
              >
                <template #content>
                  <div class="flex flex-col">
                    <div class="flex gap-2 mb-4">
                      <Button
                        v-if="post.main_photo"
                        class="p-button-danger"
                        icon="pi pi-times"
                        label="Удалить"
                        @click="onImageRemove"
                      />
                    </div>
                    <img
                      v-if="post.main_photo"
                      :src="`http://localhost:8000/static/image/${post.main_photo}`"
                      alt="Preview"
                      class="max-w-[150px] max-h-[150px] object-cover border border-gray-300 rounded"
                    />
                  </div>
                  <span v-if="!post.main_photo" class="text-red-500">Пожалуйста, выберите изображение</span>
                </template>
              </FileUpload>
            </div>
  
            <div class="flex flex-col">
              <label class="mb-2">Содержание новости</label>
              <div ref="editorContainer"></div>
            </div>
            <span v-if="post.content && post.content.length < 500" class="text-red-500 text-sm">
              Содержание должно содержать минимум 500 символов
            </span>
            <div class="flex flex-col">
              <label class="mb-2">Дата публикации</label>
              <DatePicker v-model="post.date_created" dateFormat="yy-mm-dd" />
            </div>
  
            <div class="flex flex-col sm:flex-row gap-4 mt-4">
              <Button 
                icon="pi pi-check" 
                label="Сохранить"
                @click="addPost" 
                class="p-button-warning w-full sm:w-[200px]" 
              />
              <Button 
                icon="pi pi-times" 
                label="Отмена"
                @click="visible = false" 
                class="p-button-secondary w-full sm:w-[200px]" 
              />
            </div>
        </div>
      </Sidebar>
      <Sidebar
        v-model:visible="visibledt"
        @show="initializeEditor"
        position="right"
        :style="{ width: '60rem' }"
        class="sidebar-edit"
      >
        <template #header>
          <h2>Изменить новость</h2>
        </template>
        <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50 z-50">
          <i class="pi pi-spin pi-spinner text-4xl text-white"></i>
        </div>
        <div class="flex flex-col gap-6">
            <div class="flex flex-col">
              <label class="mb-2">URL страницы (slug)</label>
              <InputText
                v-model="post.slug"
                placeholder="Введите URL страницы"
                class="w-full"
              />
            </div>
            <div class="flex flex-col">
              <label class="mb-2">H1 заголовок</label>
              <InputText
                v-model="post.h1"
                placeholder="Введите H1 заголовок"
                class="w-full"
              />
            </div>
            <div class="flex flex-col">
              <label class="mb-2">Title страницы</label>
              <InputText
                v-model="post.title"
                placeholder="Введите title страницы"
                class="w-full"
              />
            </div>
            <div class="flex flex-col">
              <label class="mb-2">Meta description</label>
              <InputText
                v-model="post.description"
                placeholder="Введите meta description"
                class="w-full"
              />
            </div>
            <div class="flex flex-col">
              <label class="mb-2">Заголовок новости</label>
              <InputText
                v-model="post.header"
                placeholder="Введите заголовок новости"
                class="w-full"
              />
              <span v-if="post.header && post.header.length < 4" class="text-red-500 text-sm"> 
                Заголовок должен содержать минимум 4 символа
              </span>
            </div>
            <div class="flex flex-col">
              <label class="mb-2">Краткое описание</label>
              <InputText
                v-model="post.summary"
                placeholder="Введите краткое описание"
                class="w-full"
              />
              <span v-if="post.summary && post.summary.length < 4" class="text-red-500 text-sm">
                Краткое описание должно содержать минимум 4 символа
              </span>
            </div>
  
            <div class="flex flex-col">
              <label class="mb-2">Изображение новости</label>
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
                  <div class="flex flex-col">
                    <div class="flex gap-2 mb-4">
                      <Button
                        v-if="post.main_photo"
                        class="p-button-danger"
                        icon="pi pi-times"
                        label="Удалить"
                        @click="onImageRemove"
                      />
                    </div>
                    <img
                      v-if="post.main_photo"
                      :src="`http://localhost:8000/static/image/${post.main_photo}`"
                      alt="Preview"
                      class="max-w-[150px] max-h-[150px] object-cover border border-gray-300 rounded"
                    />
                  </div>
                  <span v-if="!post.main_photo" class="text-red-500">Пожалуйста, выберите изображение</span>
                </template>
              </FileUpload>
            </div>
  
            <div class="flex flex-col">
              <label class="mb-2">Содержание новости</label>
              <div ref="editorContainer"></div>
            </div>
            <span v-if="post.content && post.content.length < 500" class="text-red-500 text-sm">
              Содержание должно содержать минимум 500 символов
            </span>
            <div class="flex flex-col">
              <label class="mb-2">Дата публикации</label>
              <DatePicker v-model="post.date_created" dateFormat="yy-mm-dd" />
            </div>
  
            <div class="flex flex-col sm:flex-row gap-4 mt-4">
              <Button 
                icon="pi pi-check" 
                label="Сохранить"
                @click="SaveEditedPost" 
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
      </Sidebar>
  
      <DataView
        :value="filteredNewsList"
        paginator
        :rows="10"
        dataKey="'id'"
        class="w-full"
      >
        <template #header>
          <div class="flex flex-col sm:flex-row w-full gap-4">
            <div class="flex flex-col sm:flex-row flex-1 gap-4">
              <Dropdown
                v-model="sortOrder"
                :options="sortOptions"
                optionLabel="label"
                optionValue="value"
                class="w-full sm:w-auto"
              />
              <InputText
                v-model="searchQuery"
                placeholder="Поиск по описанию"
                class="w-full"
              />
            </div>
            <Button
              icon="pi pi-plus"
              label="Добавить"
              class="p-button-warning w-full sm:w-auto"
              @click="openSidebar" 
            />
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
                  :src="`http://localhost:8000/static/image/${newsItem.main_photo}`"
                  :alt="newsItem.header"
                />
              </div>
              <div class="w-full sm:flex-1 sm:border-r sm:border-gray-200 sm:pr-4">
                <div class="text-xl font-semibold">{{ newsItem.header }}</div>
              </div>
              <div class="w-full sm:w-auto text-sm text-gray-500 sm:border-r sm:border-gray-200 sm:pr-4">
                <span>
                  {{ new Date(newsItem.date_created).toLocaleDateString() }}
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
  import { PostService, Post } from "../../api/serviceformedia";
  import { initEditor } from "../../editor.js/editor-init";
  import Dropdown from "primevue/dropdown";
  import { getToken, isAuthenticated } from "../../utils/auth";
  import { title } from "process";

  // CONSTANTS

  const router = useRouter()
  const post = ref<Post>({
    slug:"",
    h1:"",
    title:"",
    description:"",
    summary: "",
    main_photo: "",
    header: "",
    content: "",
    date_created: new Date(),
  });
  const postData = {
      slug:post.value.slug,
      h1:post.value.h1,
      title:post.value.title,
      description:post.value.description,
      content: post.value.content,
      header: post.value.header,
      summary: post.value.summary,
      main_photo: post.value.main_photo,
    };
  const token = getToken()
  const sortOrder = ref("asc");
  let previousPhoto = ""; //
  const visible = ref(false);
  const visibledt = ref(false);
  const editorContainer = ref<HTMLElement | null>(null);
  let editorInstance: any = null;
  const loading = ref(false);
  const newsList = ref<Post[]>([]);
  const postService = new PostService();
  const searchQuery = ref("");
  const sortOptions = [
    { label: "По дате(по возрастанию)", value: "asc" },
    { label: "По дате(по убыванию)", value: "desc" },
  ];
  const uploadHeaders = ref({
        'Authorization': `${token}`
      });
  
  // FUNCTIONS
  const checkAuth = () => {
  if (!isAuthenticated(token)) {
    router.push({ name: 'auth' });
    return false;
  }
  return true;
};
  const filteredNewsList = computed(() => {
    const filtered = newsList.value.filter(
      (newsItem) =>
        newsItem.summary
          .toLowerCase()
          .includes(searchQuery.value.toLowerCase()) ||
        newsItem.header.toLowerCase().includes(searchQuery.value.toLowerCase())
    );

    return filtered.sort((a, b) => {
      const dateA = new Date(a.date_created).getTime();
      const dateB = new Date(b.date_created).getTime();
      return sortOrder.value === "asc" ? dateA - dateB : dateB - dateA;
    });
  });
  const toggleSortOrder = () => {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
  };
  const resetPost = () => {
    post.value = {
      slug:"",
      h1:"",
      title:"",
      description:"",
      summary: "",
      main_photo: "",
      header: "",
      content: "",
      date_created: new Date(),
    };
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
      post.value.main_photo = "";
    }
  };
  const handleDialogClose = () => {
    if (!visible.value && post.value.main_photo) {
      deleteImage(`http://localhost:8000/static/image/${post.value.main_photo}`);
      post.value.main_photo = ""; 
    }
    if (editorInstance) {
    editorInstance.clear();
    }
  };
  const openSidebar = () => {
    visible.value = true;
    resetPost();

  };
  const SaveEditedPost = async () => {
    loading.value = true;
    if (!checkAuth()) return;
    if (!post.value.id) {
      console.error("Отсутствует ID поста");
      return;
    }
  
    post.value.content = await editorInstance
      .save()
      .then((data) => JSON.stringify(data));
    const formattedDate = post.value.date_created.toLocaleDateString("en-CA");
    const postData = {
      slug:post.value.slug,
      h1:post.value.h1,
      title:post.value.title,
      description:post.value.description,
      content: post.value.content,
      header: post.value.header,
      summary: post.value.summary,
      main_photo: post.value.main_photo,
  };
    try {
      const response = await fetch(
        `http://localhost:8000/actual/${post.value.id}`,
        {
          method: "PATCH",
          headers: {
            'Authorization': `${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ ...postData, date_created: formattedDate }),
        }
      );
  
      if (response.ok) {
        console.log("Пост успешно отредактирован");
        loadNews();
        resetPost();
        visibledt.value = false;
      } else {
        const errorData = await response.json();
        console.error("Ошибка при обновлении поста:", errorData);
      }
    } catch (error) {
      console.error("Ошибка:", error);
    }
    finally {
      loading.value = false; // Скрываем спиннер
    }
  };
  
  const loadNews = async () => {
    if (!checkAuth()) return;
    try {
      console.log(uploadHeaders)
      const response = await fetch("http://localhost:8000/actual/actual",{
        headers:{
          'Authorization': `${token}`
        }
      });
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
    loading.value = true;
    if (!checkAuth()) return;
    post.value.content = await editorInstance.save().then((data: any) => JSON.stringify(data))
  
    const content = new FormData();
  
    const formattedDate = post.value.date_created.toLocaleDateString("en-CA");
    content.append("slug", post.value.slug);
    content.append("h1", post.value.h1);
    content.append("title", post.value.title);
    content.append("description", post.value.description);
    content.append("content", post.value.content);
    content.append("header", post.value.header);
    content.append("summary", post.value.summary);
    content.append("date_created", formattedDate);
  
    if (post.value.main_photo) {
      content.append("main_photo", post.value.main_photo);
    }
  
    try {
      const response = await fetch("http://localhost:8000/actual/actual", {
        method: "POST",
        body: content,
        headers:{
          'Authorization': `${token}`
        }
      });
  
      if (response.ok) {
        console.log("Пост успешно добавлен");
        loadNews();
        post.value.slug = "";
        post.value.h1 = "";
        post.value.title = "";
        post.value.description = "";
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
    finally {
      loading.value = false; // Скрываем спиннер
    }
  };
  
  // Редактирование новости
  const editPost = (newsItem) => {
    if (!checkAuth()) return;
    post.value.slug = newsItem.slug;
    post.value.id = newsItem.id;
    post.value.h1 = newsItem.h1
    post.value.title = newsItem.title
    post.value.description = newsItem.description
    post.value.header = newsItem.header;
    post.value.summary = newsItem.summary;
    previousPhoto = newsItem.main_photo;
    post.value.main_photo = newsItem.main_photo;
    post.value.content = newsItem.content;
    post.value.date_created = new Date(newsItem.date_created);
  
    visibledt.value = true;
    initializeEditor();
    setTimeout(() => {
      try {
        const editorData = {
          blocks: JSON.parse(newsItem.content).blocks,
        };
        console.log("editorData", editorData);
        if (editorInstance) {
          editorInstance.render(editorData);
        } else {
          editorInstance.render(editorData);
        }
      } catch (error) {
        console.error("Error rendering editor data:", error);
      }
    }, 600);
  };
  
  // Удаление новости
  const deletePost = async (postId: string) => {
    if (!checkAuth()) return;
    try {
      const response = await fetch(
        `http://localhost:8000/actual/${postId}`,
        {
          method: "DELETE",
          headers:{
            'Authorization': `${token}`
          }
        }
      );
      deleteImage("http://localhost:8000/actual/actual");
  
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
    if (!checkAuth()) return;
    const imageName = fileUrl.split("/").pop();
  
    return fetch(`http://127.0.0.1:8000/admin/image/${imageName}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        'Authorization': `${token}`
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
    
  <style scoped>
  .actual-page {
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
    
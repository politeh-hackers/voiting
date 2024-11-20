<template>
  <div>
    <h1>Posts</h1>
    <DataTable :value="posts" tableStyle="min-width: 50rem">
      <Column field="id" header="ID"></Column>
      <Column field="title" header="Title"></Column>
      <Column field="content" header="Content"></Column>
    </DataTable>
  </div>
</template>

<script>
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   // optional
import Row from 'primevue/row';                   // optional

import { PostService } from "../api/service.ts";
import { onMounted } from "vue";

const service = new PostService();

export default {
  components: {
    DataTable,
    Column,
  },
  data() {
    return {
      posts: [],  // Инициализируйте как пустой массив
    };
  },
  mounted() {
    this.loadPosts("admin");
  },
  methods: {
    async loadPosts(prefix) {
      try {
        const posts = await service.getAll(prefix); 
        this.posts = posts; 
      } catch (error) {
        console.error("Ошибка загрузки постов:", error);
      }
    },
  },
};
</script>
<style scoped>

</style>

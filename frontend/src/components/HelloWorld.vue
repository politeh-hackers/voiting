<template>
  <div>
    <h1>Posts</h1>
    <ul>
      <li v-for="post in posts" :key="post.id">
        <p>{{JSON.stringify(posts)}}}</p>
        <h2>{{ post.title }}</h2>
        <p>{{ post?.content }}</p>
      </li>
    </ul>

  </div>
</template>

<script>
import axios from 'axios';
import {PostService} from "../api/service.ts";
import {onMounted} from "vue";

const service = new PostService()

export default {
  data(){
    return {
      posts: null
    }
  },
  mounted() {
    this.posts = this.loadPosts("admin")
  },
  methods: {
    async loadPosts(prefix) {
      return await service.getAll(prefix);
    }
  }
}

</script>

<template>
  <div>
    <div ref="editorContainer" class="content-editor"></div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { initEditor } from '../editor.js/editor-init'// Импортируем функцию инициализации

export default defineComponent({
  name: 'EditorComponent',
  setup() {
    const editorContainer = ref<HTMLElement | null>(null);
    let editorInstance: any = null;

    // Инициализация редактора после монтирования компонента
    onMounted(() => {
      if (editorContainer.value) {
        // Пример данных для редактора, если необходимо
        const data = null; // или можно извлечь данные из скрытого поля

        // Инициализация редактора
        editorInstance = initEditor(editorContainer.value, data);
      }
    });

    return {
      editorContainer
    };
  }
});
</script>

<style lang="scss">

</style>

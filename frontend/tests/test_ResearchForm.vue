<template>
  <div>
    <ResearchForm 
      :loading="loading" 
      @submit="handleSubmit" 
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import ResearchForm from '../src/components/ResearchForm.vue';

const loading = ref(false);
const submittedTopic = ref('');

const handleSubmit = (topic: string) => {
  submittedTopic.value = topic;
};
</script>
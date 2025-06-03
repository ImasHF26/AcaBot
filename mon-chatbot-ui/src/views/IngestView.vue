<template>
  <div class="ingest-view-container">
    <h2>Ingestion de Documents</h2>
    <p>Utilisez ce formulaire pour indexer de nouveaux documents dans le système.</p>
    <IngestForm @document-ingested="handleIngestionSuccess" />
    <div v-if="ingestionStatus" :class="['status-message', ingestionStatus.type]">
      {{ ingestionStatus.message }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import IngestForm from '@/components/Ingest/IngestForm.vue';

const ingestionStatus = ref(null); // { type: 'success' | 'error', message: '...' }

const handleIngestionSuccess = (message) => {
  ingestionStatus.value = { type: 'success', message: message };
  // Optionnel: cacher le message après quelques secondes
  setTimeout(() => ingestionStatus.value = null, 5000);
};

// Vous pourriez aussi vouloir gérer les erreurs d'ingestion ici si IngestForm les émet
</script>

<style scoped>
.ingest-view-container {
  max-width: 700px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}
p {
  text-align: center;
  color: #555;
  margin-bottom: 25px;
}
.status-message {
  margin-top: 20px;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}
.status-message.success {
  background-color: #d4edda;
  color: #155724;
  border: 1px solid #c3e6cb;
}
.status-message.error {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}
</style>
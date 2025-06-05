<template>
  <div class="documents-view-container">
    <!-- Section des Documents Ingérés -->
    <div class="section-container">
      <h2>Documents Ingérés</h2>
      <button @click="fetchDocuments" :disabled="isLoadingDocuments" class="refresh-button">
        {{ isLoadingDocuments ? '⏳ Chargement...' : '🔄 Rafraîchir les documents' }}
      </button>
      <div v-if="isLoadingDocuments" class="loading-indicator">Chargement des documents...</div>
      <div v-if="errorDocuments" class="error-message">{{ errorDocuments }}</div>
      <div v-if="!isLoadingDocuments && documents.length === 0 && !errorDocuments" class="no-documents">
        Aucun document ingéré trouvé.
      </div>
      <div class="table-container">
        <table v-if="documents.length > 0" class="documents-table">
          <thead>
            <tr>
              <th>Nom du Fichier</th>
              <th>Date d'Ingestion</th>
              <th>Département</th>
              <th>Filière</th>
              <th>Module</th>
              <th>Activité</th>
              <th>Taille Estimée (Mo)</th>
              <th>Nombre de Chunks</th>
              <th>Utilisateur</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in documents" :key="doc.id_document_reference">
              <td>{{ doc.base_filename }}</td>
              <td>{{ formatDate(doc.date_Ingestion) }}</td>
              <td>{{ doc.departement || 'N/A' }}</td>
              <td>{{ doc.filiere || 'N/A' }}</td>
              <td>{{ doc.module || 'N/A' }}</td>
              <td>{{ doc.activite || 'N/A' }}</td>
              <td>{{ doc.taille_estimee || 'N/A' }}</td>
              <td>{{ doc.nb_chunks || 'N/A' }}</td>
              <td>{{ doc.username || 'N/A' }} </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Section Historique des Conversations -->
    <div class="section-container smart-table-history-section">
      <h2>Historique des Conversations</h2>
      <button @click="loadChatHistory" :disabled="chatStore.isLoadingHistory" class="refresh-button">
        {{ chatStore.isLoadingHistory ? '⏳ Chargement de l\'historique...' : '🔄 Rafraîchir l\'historique' }}
      </button>
      <smartTable 
        :history-data="chatStore.chatHistory"
        :is-loading="chatStore.isLoadingHistory"
        :error="chatStore.fetchHistoryError"
      />
      <div v-if="!chatStore.isLoadingHistory && chatStore.fetchHistoryError && (!chatStore.chatHistory || chatStore.chatHistory.length === 0)" class="error-message">
        Erreur lors du chargement de l'historique : {{ chatStore.fetchHistoryError }}
      </div>
      <div v-if="!chatStore.isLoadingHistory && !chatStore.fetchHistoryError && (!chatStore.chatHistory || chatStore.chatHistory.length === 0)" class="no-data">
        Aucun historique trouvé.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import { useChatStore } from '@/stores/chat'; 
import smartTable from './smartTable.vue';

const documents = ref([]);
const isLoadingDocuments = ref(false);
const errorDocuments = ref(null);

const fetchDocuments = async () => {
  isLoadingDocuments.value = true;
  errorDocuments.value = null;
  try {
    const response = await api.getIngestedDocuments();
    documents.value = response.data || [];
  } catch (err) {
    errorDocuments.value = "Impossible de charger les documents ingérés. " + (err.response?.data?.detail || err.message);
    documents.value = [];
  } finally {
    isLoadingDocuments.value = false;
  }
};

const chatStore = useChatStore();

const loadChatHistory = () => {
  chatStore.fetchChatHistory({}); 
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return 'Date Invalide';
  return date.toLocaleString('fr-FR', {
    year: 'numeric', month: 'long', day: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  });
};

onMounted(() => {
  fetchDocuments();
  if ((!chatStore.chatHistory || chatStore.chatHistory.length === 0) && !chatStore.isLoadingHistory) {
     loadChatHistory();
  }
});
</script>

<style scoped>
.documents-view-container {
  padding: 24px;
  display: flex;
  flex-direction: column; 
  gap: 36px; 
  background: #f8fafc;
  min-height: 100vh;
}

.section-container {
  padding: 28px 22px 22px 22px;
  background: #fff;
  border-radius: 14px;
  border: 1.5px solid #e0e0e0;
  box-shadow: 0 4px 24px rgba(52,152,219,0.07);
}

.section-container h2 {
  text-align: center;
  margin-top: 0;
  margin-bottom: 22px;
  font-size: 1.4em;
  color: #217dbb;
  border-bottom: 1.5px solid #eaf2fb;
  padding-bottom: 10px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.refresh-button {
  margin-bottom: 18px;
  padding: 10px 18px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  display: block; 
  margin-left: auto;
  margin-right: auto;
  font-size: 1em;
  font-weight: 600;
  transition: background 0.2s;
}
.refresh-button:disabled {
  background-color: #b2bec3;
  cursor: not-allowed;
}

.loading-indicator, .no-documents, .no-data {
  text-align: center;
  padding: 18px;
  font-size: 1.08em;
  color: #555;
}

.error-message {
  color: #c0392b;
  background-color: #ffeaea;
  border: 1px solid #f5c6cb;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 18px;
  text-align: center;
  font-weight: 600;
  font-size: 1em;
}

.table-container {
  overflow-x: auto;
  margin-top: 10px;
}

.documents-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
  box-shadow: 0 2px 8px rgba(52,152,219,0.07);
  background: #f8fafc;
  border-radius: 10px;
  overflow: hidden;
}
.documents-table th, .documents-table td {
  border: 1px solid #eaf2fb;
  padding: 12px;
  text-align: left;
  font-size: 0.97em; 
}
.documents-table th {
  background-color: #eaf2fb; 
  font-weight: 700;
  color: #217dbb;
}
.documents-table tbody tr:nth-child(even) {
  background-color: #f4f8fb;
}
.documents-table tbody tr:hover {
  background-color: #d6eaff;
}

.smart-table-history-section {
  background-color: #fff;
  border-radius: 14px;   
  border: 1.5px solid #e0e0e0;
  box-shadow: 0 4px 24px rgba(52,152,219,0.07);
  padding: 28px 22px 22px 22px;
  margin-top: 20px;
  display: flex;
  flex-direction: column;
}
</style>
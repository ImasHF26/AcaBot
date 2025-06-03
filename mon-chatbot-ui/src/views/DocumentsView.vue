<template>
  <div class="documents-view-container">
    <!-- Section des Documents Ingérés (CONSERVÉE ET INCHANGÉE) -->
    <div class="section-container">
      <h2>Documents Ingérés</h2>
      <button @click="fetchDocuments" :disabled="isLoadingDocuments" class="refresh-button">
        {{ isLoadingDocuments ? 'Chargement...' : 'Rafraîchir les documents' }}
      </button>
      <div v-if="isLoadingDocuments" class="loading-indicator">Chargement des documents...</div>
      <div v-if="errorDocuments" class="error-message">{{ errorDocuments }}</div>
      
      <div v-if="!isLoadingDocuments && documents.length === 0 && !errorDocuments" class="no-documents">
        Aucun document ingéré trouvé.
      </div>

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

    <!-- Section de l'Historique des Conversations (UNIQUEMENT via smartTable) -->
    <div class="section-container smart-table-history-section">
      <h2>Historique des Conversations</h2>
      <!-- Bouton pour rafraîchir les données de l'historique qui seront passées à smartTable -->
      <button @click="loadChatHistory" :disabled="chatStore.isLoadingHistory" class="refresh-button">
        {{ chatStore.isLoadingHistory ? 'Chargement de l\'historique...' : 'Rafraîchir l\'historique' }}
      </button>
      
      <smartTable 
        :history-data="chatStore.chatHistory"
        :is-loading="chatStore.isLoadingHistory"
        :error="chatStore.fetchHistoryError"
      />
      <!-- Si smartTable gère son propre message d'erreur/chargement basé sur les props,
           vous n'avez peut-être pas besoin d'afficher chatStore.fetchHistoryError ici directement,
           sauf si vous voulez un message d'erreur global pour la section. -->
      <div v-if="!chatStore.isLoadingHistory && chatStore.fetchHistoryError && (!chatStore.chatHistory || chatStore.chatHistory.length === 0)" class="error-message">
        Erreur lors du chargement de l'historique : {{ chatStore.fetchHistoryError }}
      </div>
       <div v-if="!chatStore.isLoadingHistory && !chatStore.fetchHistoryError && (!chatStore.chatHistory || chatStore.chatHistory.length === 0)" class="no-data">
        
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import { useChatStore } from '@/stores/chat'; 
import smartTable from './smartTable.vue'; // Assurez-vous que le chemin est correct

// --- Logique pour les Documents Ingérés ---
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

// --- Logique pour l'Historique des Conversations (via Store, pour alimenter smartTable) ---
const chatStore = useChatStore();

const loadChatHistory = () => {
  // Cette fonction déclenche la récupération des données dans le store,
  // qui sont ensuite passées à smartTable via les props.
  chatStore.fetchChatHistory({}); 
};

// --- Fonctions Communes ---
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
  fetchDocuments(); // Charger les documents ingérés
  
  // Charger l'historique des conversations pour le store (qui alimentera smartTable)
  // S'assurer que chatHistory est bien un tableau avant de vérifier sa longueur
  if ((!chatStore.chatHistory || chatStore.chatHistory.length === 0) && !chatStore.isLoadingHistory) {
     loadChatHistory();
  }
});
</script>

<style scoped>
/* Vos styles existants ... */
/* Assurez-vous que les styles pour .chat-history-section, .history-list, .history-item etc. 
   sont supprimés s'ils n'étaient que pour la liste simple. 
   smartTable.vue devrait avoir ses propres styles. */

.documents-view-container {
  padding: 20px;
  display: flex;
  flex-direction: column; 
  gap: 30px; 
}

.section-container {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  border: 1px solid #eee;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.section-container h2 {
  text-align: center;
  margin-top: 0;
  margin-bottom: 20px;
  font-size: 1.5em;
  color: #333;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.refresh-button {
  margin-bottom: 20px;
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: block; 
  margin-left: auto;
  margin-right: auto;
}
.refresh-button:disabled {
  background-color: #ccc;
}

.loading-indicator, .no-documents, .no-data { /* Ajout de .no-data pour l'historique */
  text-align: center;
  padding: 20px;
  font-size: 1.1em;
  color: #555;
}

.error-message {
  color: red;
  background-color: #fdd;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
  text-align: center;
}

/* Styles pour la table des documents (inchangés) */
.documents-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.documents-table th, .documents-table td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
  font-size: 0.9em; 
}
.documents-table th {
  background-color: #e9ecef; 
  font-weight: 600;
  color: #495057;
}
.documents-table tbody tr:nth-child(even) {
  background-color: #f8f9fa;
}
.documents-table tbody tr:hover {
  background-color: #e2e6ea;
}

.smart-table-history-section {
  /* Styles spécifiques si besoin pour la section contenant smartTable */

  background-color: #f9f9f9;
  border-radius: 8px;   
  border: 1px solid #eee;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  padding: 20px;
  margin-top: 20px; /* Espacement entre les sections */
  display: flex;
  flex-direction: column;
}
</style>
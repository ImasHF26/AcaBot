<!-- smartTable.vue -->
<template>
  <div class="smart-table-container">
    <div v-if="isLoading" class="loading-indicator">
      <div class="spinner"></div>
      Chargement de l'historique...
    </div>
    <div v-else-if="error" class="error-message">
      <span class="error-icon">⚠️</span> {{ error }}
    </div>
    <div v-else-if="!processedHistory || processedHistory.length === 0" class="no-data">
      <span class="no-data-icon">ℹ️</span> Aucun historique de conversation à afficher.
    </div>
    <div v-else>
      <!-- Section des contrôles (regroupement) -->
      <div class="controls">
        <label for="groupBy">Regrouper par :</label>
        <select id="groupBy" v-model="currentGroupBy" @change="applyGroupingAndResetPage">
          <option value="">Aucun</option>
          <option value="username">Utilisateur</option>
          <option value="departement">Département</option>
          <option value="filiere">Filière</option>
          <option value="module">Module</option>
          <option value="activite">Activité</option>
        </select>
      </div>

      <!-- Affichage des données -->
      <div v-if="currentGroupBy && paginatedGroupKeys.length > 0">
        <div v-for="groupName in paginatedGroupKeys" :key="groupName" class="group-section">
          <h3 @click="toggleGroup(groupName)" class="group-header">
            <!-- Correction ici pour afficher le compte -->
            <span>{{ getGroupDisplayName(currentGroupBy, groupName) }} ({{ groupedHistory[groupName] ? groupedHistory[groupName].length : 0 }})</span>
            <span class="toggle-icon">{{ expandedGroups[groupName] ? '▲' : '▼' }}</span>
          </h3>
          <table v-if="expandedGroups[groupName]" class="history-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Utilisateur (Requête)</th>
                <th>Chatbot (Réponse)</th>
                <th>Filtres Appliqués</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in groupedHistory[groupName]" :key="item.id || item.timestamp" class="history-row">
                <td>{{ formatDate(item.timestamp) }}</td>
                <td>{{ item.user_query }} <span class="username-detail">({{ item.username || 'N/A'}})</span></td>
                <td>{{ item.chatbot_response }}</td>
                <td class="filters-cell">{{ formatFilters(item.filters) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        <PaginationControls
          :current-page="currentGroupPage"
          :total-items="totalGroups"
          :items-per-page="groupsPerPage"
          @page-changed="handleGroupPageChange"
        />
      </div>
      <div v-else-if="!currentGroupBy && paginatedItems.length > 0">
        <table class="history-table">
           <thead>
              <tr>
                <th>Date</th>
                <th>Utilisateur (Requête)</th>
                <th>Chatbot (Réponse)</th>
                
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in paginatedItems" :key="item.id || item.timestamp" class="history-row">
                <td>{{ formatDate(item.timestamp) }}</td>
                <td>{{ item.user_query }} <span class="username-detail">({{ item.username || 'N/A'}})</span></td>
                <td>{{ item.chatbot_response }}</td>
                
              </tr>
            </tbody>
        </table>
        <PaginationControls
          :current-page="currentPage"
          :total-items="totalItems"
          :items-per-page="itemsPerPage"
          @page-changed="handlePageChange"
        />
      </div>
       <div v-else-if="processedHistory.length > 0 && ( (currentGroupBy && paginatedGroupKeys.length === 0) || (!currentGroupBy && paginatedItems.length === 0) )" class="no-data">
        Aucun élément sur cette page.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, defineProps, onMounted } from 'vue';

// --- Composant interne pour la Pagination ---
const PaginationControls = {
  props: ['currentPage', 'totalItems', 'itemsPerPage'],
  emits: ['page-changed'],
  setup(props, { emit }) {
    const totalPages = computed(() => {
      if (props.itemsPerPage === 0) return 0; // Éviter la division par zéro
      return Math.ceil(props.totalItems / props.itemsPerPage);
    });
    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        emit('page-changed', page);
      }
    };
    // La pagination ne s'affiche que s'il y a plus d'une page
    const showPagination = computed(() => totalPages.value > 1);

    return { totalPages, changePage, showPagination };
  },
  template: `
    <div class="pagination-controls" v-if="showPagination">
      <button @click="changePage(currentPage - 1)" :disabled="currentPage === 1" class="pagination-button prev-next">Précédent</button>
      <span class="page-info">Page {{ currentPage }} sur {{ totalPages }}</span>
      <button @click="changePage(currentPage + 1)" :disabled="currentPage === totalPages" class="pagination-button prev-next">Suivant</button>
    </div>
  `
};

// --- Props du composant smartTable ---
const props = defineProps({
  historyData: { type: Array, default: () => [] },
  isLoading: { type: Boolean, default: false },
  error: { type: String, default: null }
});

// --- Références réactives ---
const currentGroupBy = ref('');
const groupedHistory = ref({});
const expandedGroups = ref({});

// Pagination pour les items non groupés
const currentPage = ref(1);
const itemsPerPage = ref(5); // Nombre d'items par page (5 lignes)

// Pagination pour les groupes
const currentGroupPage = ref(1);
const groupsPerPage = ref(3); // Nombre de groupes par page (vous pouvez ajuster)

// --- Données traitées et paginées ---
const processedHistory = computed(() => {
  return [...props.historyData].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
});

const totalItems = computed(() => processedHistory.value.length);
const paginatedItems = computed(() => {
  if (currentGroupBy.value) return [];
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return processedHistory.value.slice(start, end);
});

const groupKeys = computed(() => Object.keys(groupedHistory.value).sort());
const totalGroups = computed(() => groupKeys.value.length);
const paginatedGroupKeys = computed(() => {
  if (!currentGroupBy.value) return [];
  const start = (currentGroupPage.value - 1) * groupsPerPage.value;
  const end = start + groupsPerPage.value;
  return groupKeys.value.slice(start, end);
});


// --- Logique de regroupement ---
const getNestedValue = (obj, path) => {
  if (!path) return undefined;
  const keys = path.split('.');
  let result = obj;
  for (const key of keys) {
    if (result && typeof result === 'object' && key in result) {
      result = result[key];
    } else { return undefined; }
  }
  return result;
};

const applyGrouping = () => {
  if (!currentGroupBy.value) {
    groupedHistory.value = {};
    return;
  }
  const groups = {};
  processedHistory.value.forEach(item => {
    let groupKey = getNestedValue(item, currentGroupBy.value);
    groupKey = (groupKey === undefined || groupKey === null || groupKey === '') ? 'N/A' : String(groupKey);
    if (!groups[groupKey]) groups[groupKey] = [];
    groups[groupKey].push(item);
  });
  groupedHistory.value = groups;
  // Déplier les groupes par défaut lors d'un nouveau regroupement
  Object.keys(groups).forEach(key => expandedGroups.value[key] = true);
};

const applyGroupingAndResetPage = () => {
  currentPage.value = 1;
  currentGroupPage.value = 1;
  applyGrouping();
};

// --- Watchers ---
watch(() => props.historyData, () => {
  applyGroupingAndResetPage();
}, { deep: true, immediate: true });

watch(currentGroupBy, applyGroupingAndResetPage);


// --- Méthodes d'interaction ---
const toggleGroup = (groupName) => expandedGroups.value[groupName] = !expandedGroups.value[groupName];

const handlePageChange = (page) => currentPage.value = page;
const handleGroupPageChange = (page) => currentGroupPage.value = page;

// --- Fonctions de formatage ---
const getGroupDisplayName = (groupingKey, groupName) => {
  if (groupName === 'N/A') return 'Non spécifié';
  const keyName = groupingKey.split('.').pop(); 
  const displayName = keyName.charAt(0).toUpperCase() + keyName.slice(1).replace('_nom', '');
  return `${displayName}: ${groupName}`;
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString('fr-FR', { 
    year: 'numeric', month: 'short', day: 'numeric', 
    hour: '2-digit', minute: '2-digit' 
  });
};

const formatFilters = (filters) => {
  if (!filters || Object.keys(filters).length === 0) return 'Aucun';
  return Object.entries(filters)
    .filter(([, value]) => value)
    .map(([key, value]) => {
      let displayKey = key.replace('_nom', '').replace('_id', '');
      displayKey = displayKey.charAt(0).toUpperCase() + displayKey.slice(1);
      return `${displayKey}: ${value}`;
    })
    .join('; ');
};

// --- Cycle de vie ---
onMounted(() => {
  // Pour le débogage de la pagination
  // console.log("Initial totalItems:", totalItems.value);
  // console.log("Initial itemsPerPage:", itemsPerPage.value);
  // console.log("Initial totalGroups:", totalGroups.value);
  // console.log("Initial groupsPerPage:", groupsPerPage.value);
  if (props.historyData.length > 0) {
    applyGroupingAndResetPage();
  }
});

</script>

<style scoped>
/* Styles CSS de l'avant-dernière version (celle que vous préfériez) */
.smart-table-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 20px;
  background-color: #f9fafb;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  color: #374151;
}

.loading-indicator, .no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  font-size: 1.1em;
  color: #6b7280;
  text-align: center;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-left-color: #007bff; /* Bleu Abacus */
  animation: spin 1s ease infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 15px 20px;
  border-radius: 6px;
  border: 1px solid #fecaca;
  text-align: center;
  font-weight: 500;
}
.error-icon, .no-data-icon {
  font-size: 1.5em;
  margin-right: 8px;
  vertical-align: middle;
}


.controls {
  margin-bottom: 25px;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  display: flex;
  align-items: center;
}
.controls label {
  margin-right: 12px;
  font-weight: 600;
  color: #4b5563;
}
.controls select {
  padding: 10px 12px;
  border-radius: 6px;
  border: 1px solid #d1d5db;
  background-color: #fff;
  font-size: 0.95em;
  min-width: 200px;
  transition: border-color 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}
.controls select:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
  outline: none;
}

.group-section {
  margin-bottom: 25px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  overflow: hidden;
}
.group-header {
  background-color: #007bff; /* Bleu Abacus */
  color: white;
  padding: 12px 18px;
  cursor: pointer;
  margin: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 600;
  transition: background-color 0.2s ease;
}
.group-header:hover {
  background-color: #0056b3;
}
.toggle-icon {
  font-size: 0.9em;
}

.history-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 0; 
}
.history-table th, .history-table td {
  border-bottom: 1px solid #e5e7eb;
  border-left: 0;
  border-right: 0;
  padding: 14px 18px;
  text-align: left;
  font-size: 0.9em;
  vertical-align: top;
}
.history-table th {
  background-color: #f3f4f6;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  font-size: 0.8em;
  letter-spacing: 0.05em;
}
.history-table .history-row:nth-child(even) {
  background-color: #f9fafb;
}
.history-table .history-row:hover {
  background-color: #eff6ff;
}
.username-detail {
  color: #6b7280;
  font-size: 0.9em;
}
.filters-cell {
  font-size: 0.85em;
  color: #4b5563;
  line-height: 1.5;
}

/* --- Styles de Pagination (ceux de l'avant-dernière version) --- */
.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px 0;
  margin-top: 15px;
}
.pagination-button {
  background-color: #fff;
  border: 1px solid #d1d5db;
  color: #374151;
  padding: 8px 16px;
  margin: 0 5px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
  font-weight: 500;
}
.pagination-button:hover:not(:disabled) {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}
.pagination-button:disabled {
  color: #9ca3af;
  cursor: not-allowed;
  background-color: #f3f4f6;
}
.page-info {
  margin: 0 15px;
  font-size: 0.95em;
  color: #4b5563;
}
</style>
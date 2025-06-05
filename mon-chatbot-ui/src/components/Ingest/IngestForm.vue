<template>
  <form @submit.prevent="submitIngestion" class="ingest-form">
    <h3 class="form-title">Indexation d’un Document</h3>
    <div class="form-grid">
      <div class="form-group">
        <label for="base_filename">Nom du fichier de base :</label>
        <input type="text" id="base_filename" v-model="formData.base_filename" required 
               placeholder="Sera rempli par la sélection de fichier" />
      </div>

      <div class="form-group">
        <label for="file_path_display">Fichier sélectionné :</label>
        <div class="file-input-container">
          <input type="text" id="file_path_display" v-model="formData.file_path_display" disabled 
                 placeholder="Aucun fichier sélectionné" />
          <button type="button" @click="triggerLocalFileSelect" class="browse-button">📁 Parcourir…</button>
        </div>
        <input type="file" id="actual_file_input" ref="localFilePicker" @change="handleLocalFileSelected" style="display: none;"
               accept=".pdf,.txt,.docx,.md,.json" />
        <small>Choisissez un fichier local à indexer. Son nom s’affichera ci-dessus.</small>
      </div>
      
      <div class="form-group">
        <label for="ingest_departement_id">Département :</label>
        <select id="ingest_departement_id" v-model.number="formData.departement_id" required>
          <option :value="null">Sélectionner un département</option>
          <option v-for="dep in dataStore.departements" :key="dep.id" :value="dep.id">
            {{ dep.nom }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="ingest_filiere_id">Filière (optionnel) :</label>
        <select id="ingest_filiere_id" v-model.number="formData.filiere_id" :disabled="!formData.departement_id || dataStore.isLoading">
          <option :value="null">Sélectionner une filière</option>
          <option v-for="fil in dataStore.filieres" :key="fil.id" :value="fil.id">
            {{ fil.nom }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="ingest_module_id">Module (optionnel) :</label>
        <select id="ingest_module_id" v-model.number="formData.module_id" :disabled="!formData.filiere_id || dataStore.isLoading">
          <option :value="null">Sélectionner un module</option>
           <option v-for="mod in dataStore.modules" :key="mod.id" :value="mod.id">
            {{ mod.nom }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="ingest_activite_id">Activité (optionnel) :</label>
        <select id="ingest_activite_id" v-model.number="formData.activite_id">
          <option :value="null">Sélectionner une activité</option>
          <option v-for="act in dataStore.activites" :key="act.id" :value="act.id">
            {{ act.nom }}
          </option>
        </select>
      </div>
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>
    <button type="submit" :disabled="isLoading || !selectedFileObject" class="submit-button">
      {{ isLoading ? '⏳ Indexation en cours…' : '📄 Indexer le Document' }}
    </button>
  </form>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue';
import api from '@/services/api';
import { useAuthStore } from '@/stores/auth';
import { useDataStore } from '@/stores/data';

const emit = defineEmits(['document-ingested', 'ingestion-error']);
const authStore = useAuthStore();
const dataStore = useDataStore();

const formData = reactive({
  base_filename: '',
  file_path_display: '',
  departement_id: null,
  filiere_id: null,
  module_id: null,
  activite_id: null,
});

const localFilePicker = ref(null);
const selectedFileObject = ref(null);

const isLoading = ref(false);
const error = ref(null);

onMounted(() => {
  if (dataStore.departements.length === 0) dataStore.fetchDepartements();
  if (dataStore.activites.length === 0) dataStore.fetchActivites();
});

watch(() => formData.departement_id, (newDepId) => {
  formData.filiere_id = null;
  formData.module_id = null;
  if (newDepId) {
    dataStore.fetchFilieresByDepartement(newDepId);
  } else {
    dataStore.filieres = [];
    dataStore.modules = [];
  }
});

watch(() => formData.filiere_id, (newFiliereId) => {
  formData.module_id = null;
  if (newFiliereId) {
    dataStore.fetchModulesByFiliere(newFiliereId);
  } else {
    dataStore.modules = [];
  }
});

const triggerLocalFileSelect = () => {
  if (localFilePicker.value) {
    localFilePicker.value.value = null; 
  }
  localFilePicker.value?.click();
};

const handleLocalFileSelected = (event) => {
  const file = event.target.files[0];
  if (file) {
    formData.base_filename = file.name;
    formData.file_path_display = file.name;
    selectedFileObject.value = file;
    error.value = null;
  } else {
    formData.base_filename = '';
    formData.file_path_display = '';
    selectedFileObject.value = null;
  }
};

const submitIngestion = async () => {
  error.value = null;
  if (!selectedFileObject.value) {
    error.value = "Veuillez sélectionner un fichier à ingérer.";
    return;
  }
  if (!authStore.currentUser || authStore.profileId == null || authStore.userId == null) {
    error.value = "Informations utilisateur manquantes. Veuillez vous reconnecter.";
    return;
  }
  if (formData.departement_id == null) {
    error.value = "Le département est requis.";
    return;
  }
  if (!formData.base_filename) {
    error.value = "Le nom du fichier de base est manquant.";
    return;
  }

  isLoading.value = true;
  const dataPayload = new FormData();
  try {
    dataPayload.append('file_upload', selectedFileObject.value, formData.base_filename);
    dataPayload.append('base_filename', formData.base_filename);
    if (formData.departement_id != null) dataPayload.append('departement_id', formData.departement_id.toString());
    if (formData.filiere_id != null) dataPayload.append('filiere_id', formData.filiere_id.toString());
    if (formData.module_id != null) dataPayload.append('module_id', formData.module_id.toString());
    if (formData.activite_id != null) dataPayload.append('activite_id', formData.activite_id.toString());
    dataPayload.append('profile_id', authStore.profileId.toString());
    dataPayload.append('user_id', authStore.userId.toString());
  } catch (e) {
    error.value = "Erreur interne lors de la préparation des données.";
    isLoading.value = false;
    return;
  }

  try {
    const response = await api.ingestDocument(dataPayload); 
    if (response.data && response.data.status === 'success') {
      emit('document-ingested', response.data.message || 'Document indexé avec succès!');
      formData.base_filename = '';
      formData.file_path_display = '';
      selectedFileObject.value = null;
      if (localFilePicker.value) localFilePicker.value.value = null;
      formData.departement_id = null;
      formData.filiere_id = null;
      formData.module_id = null;
      formData.activite_id = null;
    } else {
      error.value = response.data?.message || response.data?.detail || "Erreur lors de l'indexation.";
      emit('ingestion-error', error.value);
    }
  } catch (err) {
    if (err.response && err.response.data && err.response.data.detail) {
        if (Array.isArray(err.response.data.detail)) {
            error.value = err.response.data.detail.map(d => `${d.loc.join('.')} - ${d.msg}`).join('; ');
        } else {
            error.value = err.response.data.detail;
        }
    } else {
        error.value = err.message || "Une erreur serveur est survenue.";
    }
    emit('ingestion-error', error.value);
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.ingest-form {
  background: #fff;
  padding: 32px 28px 24px 28px;
  border-radius: 14px;
  box-shadow: 0 8px 32px rgba(52,152,219,0.13);
  max-width: 700px;
  margin: 32px auto;
}

.form-title {
  color: #217dbb;
  font-size: 1.5em;
  font-weight: 700;
  margin-bottom: 24px;
  text-align: center;
  letter-spacing: 1px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 22px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  font-weight: 500;
  color: #217dbb;
}

.form-group input[type="text"],
.form-group select {
  padding: 10px;
  border: 1.5px solid #d6eaff;
  border-radius: 6px;
  font-size: 1em;
  background: #f8fafc;
  transition: border-color 0.2s;
}
.form-group input[type="text"]:disabled {
  background-color: #e9ecef;
  opacity: 0.7;
  cursor: not-allowed;
}
.form-group select:disabled {
  background-color: #e9ecef;
}

.form-group small {
  font-size: 0.85em;
  color: #666;
  margin-top: 5px;
}

.file-input-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.file-input-container input[type="text"] {
  flex-grow: 1;
}

.browse-button {
  padding: 10px 15px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1em;
  font-weight: 600;
  transition: background-color 0.2s;
  display: flex;
  align-items: center;
  gap: 0.3em;
}
.browse-button:hover {
  background-color: #217dbb;
}

.submit-button {
  display: block;
  width: 100%;
  padding: 14px 0;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.15em;
  font-weight: 700;
  margin-top: 18px;
  transition: background-color 0.3s;
}
.submit-button:hover:not(:disabled) {
  background-color: #219150;
}
.submit-button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

.error-message {
  color: #c0392b;
  background: #ffeaea;
  border: 1px solid #f5c6cb;
  margin-bottom: 15px;
  text-align: center;
  padding: 10px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 1em;
}
</style>
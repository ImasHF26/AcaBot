<template>
  <form @submit.prevent="submitIngestion" class="ingest-form">
    <div class="form-grid">
      <div class="form-group">
        <label for="base_filename">Nom du fichier de base :</label>
        <input type="text" id="base_filename" v-model="formData.base_filename" required 
               placeholder="Sera rempli par la sélection de fichier" />
      </div>

      <div class="form-group">
        <label for="file_path_display">Fichier sélectionné :</label> <!-- Label ajusté -->
        <div class="file-input-container">
          <!-- Ce champ affiche le nom du fichier sélectionné, il n'est plus un chemin serveur -->
          <input type="text" id="file_path_display" v-model="formData.file_path_display" disabled 
                 placeholder="Aucun fichier sélectionné" />
          <button type="button" @click="triggerLocalFileSelect" class="browse-button">Parcourir...</button>
        </div>
        <!-- Input de type file caché, déclenché par le bouton -->
        <input type="file" id="actual_file_input" ref="localFilePicker" @change="handleLocalFileSelected" style="display: none;"
               accept=".pdf,.txt,.docx,.md,.json" />
        <small>"Parcourir..." sélectionne un fichier local. Son nom sera affiché ci-dessus.</small>
      </div>
      
      <!-- Les autres champs (Département, Filière, etc.) restent identiques -->
      <div class="form-group">
        <label for="ingest_departement_id">Département:</label>
        <select id="ingest_departement_id" v-model.number="formData.departement_id" @change="onDepartementChange" required>
          <option :value="null">Sélectionner un département</option>
          <option v-for="dep in dataStore.departements" :key="dep.id" :value="dep.id">
            {{ dep.nom }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="ingest_filiere_id">Filière (optionnel):</label>
        <select id="ingest_filiere_id" v-model.number="formData.filiere_id" :disabled="!formData.departement_id || dataStore.isLoading">
          <option :value="null">Sélectionner une filière</option>
          <option v-for="fil in dataStore.filieres" :key="fil.id" :value="fil.id">
            {{ fil.nom }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="ingest_module_id">Module (optionnel):</label>
        <select id="ingest_module_id" v-model.number="formData.module_id" :disabled="!formData.filiere_id || dataStore.isLoading">
          <option :value="null">Sélectionner un module</option>
           <option v-for="mod in dataStore.modules" :key="mod.id" :value="mod.id">
            {{ mod.nom }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="ingest_activite_id">Activité (optionnel):</label>
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
      {{ isLoading ? 'Indexation en cours...' : 'Indexer le Document' }}
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

// onDepartementChange n'est plus explicitement nécessaire si la logique est dans le watcher
// const onDepartementChange = () => { /* Logique dans le watcher */ };

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
    console.log(`Fichier sélectionné: ${file.name}, Type: ${file.type}, Taille: ${file.size} bytes`);
  } else {
    formData.base_filename = '';
    formData.file_path_display = '';
    selectedFileObject.value = null;
  }
};

const submitIngestion = async () => {
  console.log("--- Début de submitIngestion ---");
  console.log("Valeurs initiales pour la soumission:");
  console.log("authStore.currentUser:", authStore.currentUser);
  console.log("authStore.profileId:", authStore.profileId, "(Type:", typeof authStore.profileId, ")");
  console.log("authStore.userId:", authStore.userId, "(Type:", typeof authStore.userId, ")"); // LOG CRUCIAL
  console.log("selectedFileObject.value:", selectedFileObject.value ? selectedFileObject.value.name : 'null');
  console.log("formData.departement_id:", formData.departement_id, "(Type:", typeof formData.departement_id, ")");
  console.log("formData.base_filename:", formData.base_filename);

  error.value = null; // Réinitialiser l'erreur au début

  if (!selectedFileObject.value) {
    error.value = "Veuillez sélectionner un fichier à ingérer.";
    console.error("Validation échouée: Aucun fichier sélectionné.");
    return;
  }

  // Validation plus stricte pour les IDs de l'utilisateur
  if (!authStore.currentUser || 
      authStore.profileId === null || authStore.profileId === undefined || 
      authStore.userId === null || authStore.userId === undefined) {
    error.value = "Informations utilisateur (profileId ou userId) manquantes ou invalides. Veuillez vous reconnecter.";
    console.error("Validation échouée: Informations utilisateur manquantes.", 
                  "profileId:", authStore.profileId, "userId:", authStore.userId);
    return;
  }

  if (formData.departement_id === null || formData.departement_id === undefined) {
    error.value = "Le département est requis.";
    console.error("Validation échouée: Département non sélectionné.");
    return;
  }

  if (!formData.base_filename) {
    error.value = "Le nom du fichier de base est manquant (ne devrait pas arriver si un fichier est sélectionné).";
    console.error("Validation échouée: Nom de fichier de base manquant.");
    return;
  }

  isLoading.value = true;

  const dataPayload = new FormData();
  
  try {
    console.log("Construction de FormData...");
    dataPayload.append('file_upload', selectedFileObject.value, formData.base_filename);
    console.log("Append file_upload:", selectedFileObject.value.name);

    dataPayload.append('base_filename', formData.base_filename);
    console.log("Append base_filename:", formData.base_filename);

    if (formData.departement_id !== null) { // Déjà validé mais bonne pratique
        dataPayload.append('departement_id', formData.departement_id.toString());
        console.log("Append departement_id:", formData.departement_id.toString());
    }
    
    // Pour les champs optionnels, s'assurer qu'ils ne sont pas null avant toString()
    // FastAPI gère bien les Optional[int] = Form(None), donc envoyer null est ok, mais pas via .toString()
    // Si le backend attend une chaîne vide pour "non fourni" ou rien du tout, ajuster ici.
    // Pour l'instant, on s'assure juste de ne pas faire .toString() sur null.
    if (formData.filiere_id !== null && formData.filiere_id !== undefined) {
        dataPayload.append('filiere_id', formData.filiere_id.toString());
        console.log("Append filiere_id:", formData.filiere_id.toString());
    }
    if (formData.module_id !== null && formData.module_id !== undefined) {
        dataPayload.append('module_id', formData.module_id.toString());
        console.log("Append module_id:", formData.module_id.toString());
    }
    if (formData.activite_id !== null && formData.activite_id !== undefined) {
        dataPayload.append('activite_id', formData.activite_id.toString());
        console.log("Append activite_id:", formData.activite_id.toString());
    }
    
    // Ces deux lignes sont critiques. Les validations ci-dessus devraient les protéger.
    dataPayload.append('profile_id', authStore.profileId.toString());
    console.log("Append profile_id:", authStore.profileId.toString());

    dataPayload.append('user_id', authStore.userId.toString()); 
    console.log("Append user_id:", authStore.userId.toString());

  } catch (e) {
    console.error("--- Erreur critique lors de la construction de FormData ---:", e);
    error.value = "Erreur interne lors de la préparation des données. Vérifiez la console pour les détails. Cause probable: ID utilisateur ou profile manquant.";
    isLoading.value = false;
    return; // Arrêter ici si la construction échoue
  }
  
  console.log("--- Contenu final de dataPayload avant envoi ---:");
  for (let pair of dataPayload.entries()) {
      if (pair[1] instanceof File) {
          console.log(pair[0] + ': File (name: ' + pair[1].name + ', size: ' + pair[1].size + ')');
      } else {
          console.log(pair[0] + ': ' + pair[1]);
      }
  }

  try {
    console.log("--- Envoi des données FormData pour ingestion... ---");
    const response = await api.ingestDocument(dataPayload); 
    
    console.log("Réponse de l'API d'ingestion:", response);

    if (response.data && response.data.status === 'success') {
      emit('document-ingested', response.data.message || 'Document indexé avec succès!');
      // Réinitialiser le formulaire
      formData.base_filename = '';
      formData.file_path_display = '';
      selectedFileObject.value = null;
      if (localFilePicker.value) localFilePicker.value.value = null;
      formData.departement_id = null;
      formData.filiere_id = null;
      formData.module_id = null;
      formData.activite_id = null;
    } else {
      error.value = response.data?.message || response.data?.detail || "Erreur lors de l'indexation (réponse non-success).";
      console.error("Erreur d'indexation (réponse non-success):", response.data);
      emit('ingestion-error', error.value);
    }
  } catch (err) {
    console.error("--- Erreur lors de la soumission de l'ingestion (catch) ---:", err);
    console.error("Erreur response:", err.response);
    console.error("Erreur request:", err.request);
    console.error("Erreur message:", err.message);
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
    console.log("--- Fin de submitIngestion ---");
  }
};
</script>

<style scoped>
/* Vos styles existants, y compris .file-input-container et .browse-button */
.ingest-form {
  background-color: #f9f9f9;
  padding: 25px;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-group input[type="text"],
.form-group input[type="file"], /* Au cas où vous le rendez visible */
.form-group select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
}
.form-group input[type="text"]:disabled { /* Style pour les champs désactivés */
  background-color: #e9ecef;
  opacity: 0.7;
  cursor: not-allowed;
}
.form-group select:disabled {
  background-color: #e9ecef;
}

.form-group small {
  font-size: 0.8em;
  color: #666;
  margin-top: 5px;
}

.submit-button {
  display: block;
  width: 100%;
  padding: 12px 20px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1.1em;
  transition: background-color 0.3s ease;
}

.submit-button:hover:not(:disabled) {
  background-color: #218838;
}

.submit-button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

.error-message {
  color: red;
  margin-bottom: 15px;
  text-align: center;
  background-color: #fdd;
  padding: 8px;
  border-radius: 4px;
}

.file-input-container {
  display: flex;
  align-items: center;
}

.file-input-container input[type="text"] { /* S'applique à file_path_display */
  flex-grow: 1;
  margin-right: 8px;
}

.browse-button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  white-space: nowrap;
}

.browse-button:hover {
  background-color: #0056b3;
}
</style>
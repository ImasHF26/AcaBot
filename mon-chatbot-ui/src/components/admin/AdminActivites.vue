<template>
  <div class="admin-page">
    <h3>Gestion des Activités</h3>

    <!-- Zone de notification -->
    <div v-if="notification.message" :class="['alert', notification.type === 'success' ? 'alert-success' : 'alert-danger', 'mt-3']" role="alert">
      {{ notification.message }}
      <button type="button" class="btn-close" @click="clearNotification" aria-label="Close"></button>
    </div>

    <button @click="openAddModal" class="btn btn-primary mb-3 mt-3" :disabled="isLoadingInitialData">
      <span v-if="isLoadingInitialData" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
      Ajouter une Activité
    </button>

    <div v-if="dataStore.isLoading && activites.length === 0" class="text-center mt-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Chargement des données...</span>
      </div>
      <p class="mt-2">Chargement des activités...</p>
    </div>

    <div v-else-if="activites.length === 0 && !dataStore.isLoading" class="alert alert-info text-center mt-3">
      Aucune activité trouvée. Vous pouvez en ajouter une en utilisant le bouton ci-dessus.
    </div>

    <table v-else class="table table-striped table-hover">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nom</th>
          <!-- <th>Module Associé</th> -->
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="act in activites" :key="act.id">
          <td>{{ act.id }}</td>
          <td>{{ act.nom }}</td>
          <!-- <td>{{ act.module_id ? getModuleName(act.module_id) : 'Aucun' }}</td> -->
          <td>
            <button @click="editActivite(act)" class="btn btn-sm btn-warning me-2" :disabled="isLoadingAction">
              <i class="bi bi-pencil-fill"></i> Modifier
            </button>
            <button @click="confirmDelete(act.id, 'activité')" class="btn btn-sm btn-danger" :disabled="isLoadingAction">
              <i class="bi bi-trash-fill"></i> Supprimer
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal pour Ajout/Modification -->
    <div v-if="showModal" class="modal-backdrop">
      <div class="modal-content">
        <h4>{{ isEditMode ? 'Modifier l\'Activité' : 'Ajouter une Activité' }}</h4>
        <form @submit.prevent="handleSubmit">
          <div v-if="formErrorMessage" class="alert alert-danger">
            {{ formErrorMessage }}
          </div>
          <div class="mb-3">
            <label for="activiteNom" class="form-label">Nom de l'Activité:</label>
            <input type="text" id="activiteNom" v-model="form.nom" class="form-control" :class="{'is-invalid': formErrors.nom}" required>
            <div v-if="formErrors.nom" class="invalid-feedback">{{ formErrors.nom }}</div>
          </div>
          <div class="mb-3">
            <label for="activiteModule" class="form-label">Module (Optionnel):</label>
            <select id="activiteModule" v-model="form.module_id" class="form-control">
              <option value="">Aucun module spécifique</option>
              <option v-for="mod in modulesForSelect" :key="mod.id" :value="mod.id">
                {{ mod.nom }} ({{ getFiliereNameForModule(mod.filiere_id) }})
              </option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn btn-success" :disabled="isLoadingAction">
              <span v-if="isLoadingAction" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              {{ isEditMode ? 'Mettre à jour' : 'Ajouter' }}
            </button>
            <button type="button" @click="closeModal" class="btn btn-secondary ms-2" :disabled="isLoadingAction">Annuler</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue';
import { useDataStore } from '@/stores/data'; // Assurez-vous que le chemin est correct

const dataStore = useDataStore();

const activites = computed(() => dataStore.adminActivites);
const modulesForSelect = computed(() => dataStore.adminModules);
const filieresForModuleSelect = computed(() => dataStore.adminFilieres);

// États de chargement
const isLoadingInitialData = ref(true); // Pour le chargement initial des données de la page
const isLoadingAction = ref(false); // Pour les actions CRUD (ajout, modif, suppression)

// Notifications
const notification = reactive({ message: '', type: '' }); // type: 'success' ou 'danger'

// Gestion du Modal
const showModal = ref(false);
const isEditMode = ref(false);
const currentActiviteId = ref(null);

// Formulaire et erreurs
const form = reactive({
  nom: '',
  module_id: '',
});
const formErrors = reactive({});
const formErrorMessage = ref(''); // Message d'erreur général pour le formulaire

const clearNotification = () => {
  notification.message = '';
  notification.type = '';
};

const showNotification = (message, type = 'success', duration = 5000) => {
  notification.message = message;
  notification.type = type;
  if (duration > 0) {
    setTimeout(clearNotification, duration);
  }
};

onMounted(async () => {
  console.log("AdminActivites.vue: Component Mounted.");
  isLoadingInitialData.value = true;
  try {
    // Charger les données nécessaires en parallèle si possible
    await Promise.all([
      dataStore.adminFilieres.length === 0 ? dataStore.fetchAdminAllFilieres() : Promise.resolve(),
      dataStore.adminModules.length === 0 ? dataStore.fetchAdminAllModules() : Promise.resolve()
    ]);
    await dataStore.fetchAdminAllActivites(true); // Charger les activités après les dépendances
    console.log("AdminActivites.vue: After fetchAdminAllActivites, adminActivites in store:", dataStore.adminActivites);
  } catch (error) {
    console.error("Erreur lors du chargement initial des données:", error);
    showNotification("Erreur lors du chargement des données initiales. Veuillez réessayer.", "danger", 0);
  } finally {
    isLoadingInitialData.value = false;
  }
});

const getModuleName = (moduleId) => {
  if (!moduleId) return 'N/A';
  const mod = modulesForSelect.value.find(m => m.id === moduleId); // Utiliser modulesForSelect qui est déjà chargé
  return mod ? mod.nom : 'Module inconnu';
};

const getFiliereNameForModule = (filiereId) => {
  const filiere = filieresForModuleSelect.value.find(f => f.id === filiereId);
  return filiere ? filiere.nom : 'Filière N/A';
};

const resetForm = () => {
  form.nom = '';
  form.module_id = '';
  currentActiviteId.value = null;
  formErrorMessage.value = '';
  for (const key in formErrors) {
    delete formErrors[key];
  }
};

const openAddModal = () => {
  isEditMode.value = false;
  resetForm();
  showModal.value = true;
};

const editActivite = (act) => {
  isEditMode.value = true;
  resetForm(); // S'assurer que les erreurs précédentes sont effacées
  currentActiviteId.value = act.id;
  form.nom = act.nom;
  form.module_id = act.module_id || '';
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  resetForm();
};

const validateForm = () => {
  let isValid = true;
  formErrorMessage.value = '';
  for (const key in formErrors) {
    delete formErrors[key];
  }

  if (!form.nom.trim()) {
    formErrors.nom = "Le nom de l'activité est requis.";
    isValid = false;
  }
  // Ajoutez d'autres validations si nécessaire
  return isValid;
};

const handleSubmit = async () => {
  if (!validateForm()) {
    return;
  }

  isLoadingAction.value = true;
  formErrorMessage.value = ''; // Clear previous general errors

  try {
    const payload = {
      nom: form.nom.trim(),
      module_id: form.module_id ? parseInt(form.module_id, 10) : null,
    };

    if (isEditMode.value && currentActiviteId.value) {
      await dataStore.updateActivite(currentActiviteId.value, payload);
      showNotification('Activité mise à jour avec succès!', 'success');
    } else {
      await dataStore.createActivite(payload);
      showNotification('Activité ajoutée avec succès!', 'success');
    }
    closeModal();
  } catch (error) {
    console.error("Erreur lors de la soumission de l'activité:", error);
    const detail = error.response?.data?.detail || error.message || "Une erreur inconnue s'est produite.";
    formErrorMessage.value = `Erreur: ${detail}`; // Afficher l'erreur dans le modal
    showNotification(`Erreur lors de la soumission: ${detail}`, 'danger', 0); // Aussi en notification globale si besoin
  } finally {
    isLoadingAction.value = false;
  }
};

const confirmDelete = async (id, type) => {
  if (window.confirm(`Êtes-vous sûr de vouloir supprimer cette ${type} (ID: ${id}) ? Cette action est irréversible.`)) {
    isLoadingAction.value = true;
    try {
      if (type === 'activité') {
        await dataStore.deleteActivite(id);
        showNotification(`${type.charAt(0).toUpperCase() + type.slice(1)} supprimée avec succès!`, 'success');
      }
    } catch (error) {
      console.error(`Erreur lors de la suppression de l'${type}:`, error);
      const detail = error.response?.data?.detail || error.message || "Une erreur inconnue s'est produite.";
      showNotification(`Erreur lors de la suppression: ${detail}`, 'danger', 0);
    } finally {
      isLoadingAction.value = false;
    }
  }
};

</script>

<style scoped>
.admin-page {
  padding: 20px;
  max-width: 1140px; /* Augmenté de 900px à 1140px, ajustez selon vos besoins */
  margin: auto; /* Centrer la page */
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6); /* Fond légèrement plus sombre */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}

.modal-content {
  background-color: white;
  padding: 25px; /* Un peu plus de padding */
  border-radius: 8px; /* Coins plus arrondis */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2); /* Ombre plus prononcée */
  width: 90%;
  max-width: 500px;
}

.modal-actions {
  margin-top: 25px; /* Plus d'espace avant les boutons */
  text-align: right;
}

.table {
  margin-top: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1); /* Légère ombre pour le tableau */
  border-radius: 8px; /* Coins arrondis */
  overflow: hidden; /* Pour arrondir les coins du tableau */
  width: 100%;
  font-size: 1.1rem; /* Taille de police légèrement plus grande */
}

.table th,
.table td {
  text-align: center; /* Centrer le texte dans les en-têtes et les cellules */
  vertical-align: middle; /* Optionnel: pour mieux centrer verticalement si les cellules ont des hauteurs variables */
  padding: 0.75rem; /* Ajuster le padding si nécessaire avec la nouvelle taille de police */
}

.table th {
  background-color: #f8f9fa;
  font-weight: 600; /* Rendre les en-têtes un peu plus gras */
}

.btn {
  display: inline-flex; /* Pour aligner le spinner et le texte */
  align-items: center;
  gap: 0.5rem; /* Espace entre l'icône/spinner et le texte */
}

.btn-primary { background-color: #007bff; border-color: #007bff; }
.btn-warning { color: #212529; background-color: #ffc107; border-color: #ffc107; }
.btn-danger { background-color: #dc3545; border-color: #dc3545; }
.btn-success { background-color: #28a745; border-color: #28a745; }
.btn-secondary { background-color: #6c757d; border-color: #6c757d; }

.mb-3 { margin-bottom: 1rem !important; }
.mt-3 { margin-top: 1rem !important; }
.me-2 { margin-right: 0.5rem !important; }
.ms-2 { margin-left: 0.5rem !important; }

.form-label { margin-bottom: 0.5rem; font-weight: 500; } /* Label un peu plus en évidence */
.form-control {
  display: block;
  width: 100%;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: #212529;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  transition: border-color .15s ease-in-out, box-shadow .15s ease-in-out;
}
.form-control:focus {
  border-color: #86b7fe;
  outline: 0;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, .25);
}
.form-control.is-invalid {
  border-color: #dc3545; /* Couleur de bordure pour erreur Bootstrap */
}
.invalid-feedback {
  display: block; /* S'assurer que le message d'erreur est visible */
  width: 100%;
  margin-top: 0.25rem;
  font-size: .875em;
  color: #dc3545; /* Couleur de texte pour erreur Bootstrap */
}

.text-center { text-align: center; }

/* Styles pour la notification */
.alert {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.btn-close {
  padding: 0.5rem; /* Augmenter la zone cliquable */
}

/* Pour les icônes Bootstrap (si vous les utilisez) */
/* @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.8.1/font/bootstrap-icons.css"); */
/* Si vous n'utilisez pas Bootstrap Icons globalement, vous pouvez les omettre ou les ajouter */
/* J'ai ajouté des classes bi-* pour l'exemple, vous aurez besoin de la librairie d'icônes */

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
  border-width: .2em;
}
</style>
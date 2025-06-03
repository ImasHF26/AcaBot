<template>
  <div class="admin-page">
    <h3>Gestion des Modules</h3>
    <button @click="openAddModal" class="btn btn-primary mb-3">Ajouter un Module</button>

    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nom</th>
          <th>Filière</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="dataStore.isLoading && modules.length === 0">
          <td colspan="4" class="text-center">Chargement...</td>
        </tr>
        <tr v-else-if="modules.length === 0">
          <td colspan="4" class="text-center">Aucun module trouvé.</td>
        </tr>
        <tr v-for="mod in modules" :key="mod.id">
          <td>{{ mod.id }}</td>
          <td>{{ mod.nom }}</td>
          <td>{{ getFiliereName(mod.filiere_id) }}</td>
          <td>
            <button @click="editModule(mod)" class="btn btn-sm btn-warning me-2">Modifier</button>
            <button @click="confirmDelete(mod.id, 'module')" class="btn btn-sm btn-danger">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal pour Ajout/Modification -->
    <div v-if="showModal" class="modal-backdrop">
      <div class="modal-content">
        <h4>{{ isEditMode ? 'Modifier le Module' : 'Ajouter un Module' }}</h4>
        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label for="moduleNom" class="form-label">Nom du Module:</label>
            <input type="text" id="moduleNom" v-model="form.nom" class="form-control" required>
          </div>
          <div class="mb-3">
            <label for="moduleFiliere" class="form-label">Filière:</label>
            <select id="moduleFiliere" v-model="form.filiere_id" class="form-control" required>
              <option disabled value="">Choisissez une filière</option>
              <option v-for="filiere in filieresForSelect" :key="filiere.id" :value="filiere.id">
                {{ filiere.nom }} ({{ getDepartementNameForFiliere(filiere.departement_id) }})
              </option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn btn-success">{{ isEditMode ? 'Mettre à jour' : 'Ajouter' }}</button>
            <button type="button" @click="closeModal" class="btn btn-secondary ms-2">Annuler</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, reactive } from 'vue';
import { useDataStore } from '@/stores/data';

const dataStore = useDataStore();

const modules = computed(() => dataStore.adminModules);
const filieresForSelect = computed(() => dataStore.adminFilieres);
// Pour afficher le nom du département à côté de la filière dans le select
const departementsForFiliereSelect = computed(() => dataStore.adminDepartements);


onMounted(async () => {
  console.log("AdminModules.vue: Component Mounted.");
  // Charger les départements (nécessaire pour getDepartementNameForFiliere)
  if (dataStore.adminDepartements.length === 0) {
      await dataStore.fetchAdminAllDepartements();
  }
  // Charger les filières pour le select du formulaire
  if (dataStore.adminFilieres.length === 0) {
      await dataStore.fetchAdminAllFilieres();
  }
  // Charger TOUS les modules pour la liste principale
  await dataStore.fetchAdminAllModules(true);
  console.log("AdminModules.vue: After fetchAdminAllModules, adminModules in store:", dataStore.adminModules);
});

const getFiliereName = (filiereId) => {
  const filiere = dataStore.adminFilieres.find(f => f.id === filiereId);
  return filiere ? filiere.nom : 'N/A';
};

const getDepartementNameForFiliere = (departementId) => {
  const dept = departementsForFiliereSelect.value.find(d => d.id === departementId);
  return dept ? dept.nom : 'Dept N/A';
};


const showModal = ref(false);
const isEditMode = ref(false);
const currentModuleId = ref(null);

const form = reactive({
  nom: '',
  filiere_id: '', // Assurez-vous que c'est le nom attendu par l'API
});

const resetForm = () => {
  form.nom = '';
  form.filiere_id = '';
  currentModuleId.value = null;
};

const openAddModal = () => {
  isEditMode.value = false;
  resetForm();
  showModal.value = true;
};

const editModule = (mod) => {
  isEditMode.value = true;
  currentModuleId.value = mod.id;
  form.nom = mod.nom;
  form.filiere_id = mod.filiere_id;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  resetForm();
};

const handleSubmit = async () => {
  if (!form.nom.trim() || !form.filiere_id) {
    alert("Tous les champs sont requis.");
    return;
  }
  try {
    const payload = { nom: form.nom, filiere_id: parseInt(form.filiere_id) };
    if (isEditMode.value && currentModuleId.value) {
      await dataStore.updateModule(currentModuleId.value, payload);
    } else {
      await dataStore.createModule(payload);
    }
    closeModal();
  } catch (error) {
    console.error("Erreur lors de la soumission du module:", error);
    alert("Erreur lors de la soumission: " + (error.response?.data?.detail || error.message));
  }
};

const confirmDelete = async (id, type) => {
  if (window.confirm(`Êtes-vous sûr de vouloir supprimer ce ${type} (ID: ${id}) ?`)) {
    try {
      if (type === 'module') {
        await dataStore.deleteModule(id);
      }
    } catch (error) {
      console.error(`Erreur lors de la suppression du ${type}:`, error);
      alert(`Erreur lors de la suppression: ` + (error.response?.data?.detail || error.message));
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
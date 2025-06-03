<template>
  <div class="admin-page">
    <h3>Gestion des Départements</h3>
    <button @click="openAddModal" class="btn btn-primary mb-3">Ajouter un Département</button>

    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nom</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="dataStore.isLoading">
          <td colspan="3" class="text-center">Chargement...</td>
        </tr>
        <tr v-else-if="departements.length === 0">
          <td colspan="3" class="text-center">Aucun département trouvé.</td>
        </tr>
        <tr v-for="dept in departements" :key="dept.id">
          <td>{{ dept.id }}</td>
          <td>{{ dept.nom }}</td>
          <td>
            <button @click="editDepartement(dept)" class="btn btn-sm btn-warning me-2">Modifier</button>
            <button @click="confirmDelete(dept.id, 'departement')" class="btn btn-sm btn-danger">Supprimer</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Modal pour Ajout/Modification -->
    <div v-if="showModal" class="modal-backdrop">
      <div class="modal-content">
        <h4>{{ isEditMode ? 'Modifier le Département' : 'Ajouter un Département' }}</h4>
        <form @submit.prevent="handleSubmit">
          <div class="mb-3">
            <label for="deptNom" class="form-label">Nom du Département:</label>
            <input type="text" id="deptNom" v-model="form.nom" class="form-control" required>
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

// Utiliser l'état admin pour l'affichage de la liste
const departements = computed(() => dataStore.adminDepartements);

const showModal = ref(false);
const isEditMode = ref(false);
const currentDepartementId = ref(null);

const form = reactive({
  nom: '',
});

onMounted(async () => {
  console.log("AdminDepartements.vue: Component Mounted.");
  await dataStore.fetchAdminAllDepartements(true); // true pour forcer pendant le dev
  console.log("AdminDepartements.vue: After fetchAdminAllDepartements, adminDepartements in store:", dataStore.adminDepartements);
});

const resetForm = () => {
  form.nom = '';
  currentDepartementId.value = null;
};

const openAddModal = () => {
  isEditMode.value = false;
  resetForm();
  showModal.value = true;
};

const editDepartement = (dept) => {
  isEditMode.value = true;
  currentDepartementId.value = dept.id;
  form.nom = dept.nom;
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  resetForm();
};

const handleSubmit = async () => {
  if (!form.nom.trim()) {
    alert("Le nom du département ne peut pas être vide.");
    return;
  }
  try {
    if (isEditMode.value && currentDepartementId.value) {
      await dataStore.updateDepartement(currentDepartementId.value, { nom: form.nom });
    } else {
      await dataStore.createDepartement({ nom: form.nom });
    }
    closeModal();
    // La liste se mettra à jour car fetchAdminAllDepartements est appelé dans les actions CRUD du store
  } catch (error) {
    console.error("Erreur lors de la soumission du département:", error);
    alert("Erreur lors de la soumission: " + (error.response?.data?.detail || error.message));
  }
};

const confirmDelete = async (id, type) => {
  if (window.confirm(`Êtes-vous sûr de vouloir supprimer ce ${type} (ID: ${id}) ?`)) {
    try {
      if (type === 'departement') {
        await dataStore.deleteDepartement(id);
      }
      // La liste se mettra à jour
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
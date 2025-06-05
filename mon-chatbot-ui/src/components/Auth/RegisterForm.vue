<template>
  <div class="admin-users-page">
    <h3>Gestion des Utilisateurs</h3>
    <button @click="openAddModal" class="btn btn-primary mb-3">
      <span class="btn-emoji">➕</span> Ajouter un Utilisateur
    </button>

    <!-- Section de Filtres -->
    <div class="filters-section card mb-3">
      <div class="card-body">
        <h5 class="card-title">Filtres</h5>
        <div class="row g-3">
          <div class="col-md-4">
            <label for="searchQuery" class="form-label">Rechercher (Nom d'utilisateur)</label>
            <input type="text" id="searchQuery" v-model="searchQuery" class="form-control" placeholder="Nom d'utilisateur...">
          </div>
          <div class="col-md-3">
            <label for="filterStatus" class="form-label">Statut du compte</label>
            <select id="filterStatus" v-model="filterStatus" class="form-select">
              <option value="">Tous</option>
              <option :value="true">Actif</option>
              <option :value="false">Inactif</option>
            </select>
          </div>
          <div class="col-md-3">
            <label for="filterProfile" class="form-label">Profil</label>
            <select id="filterProfile" v-model="filterProfileId" class="form-select">
              <option value="">Tous</option>
              <option value="1">Admin</option>
              <option value="2">Prof</option>
              <option value="3">Étudiant</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <div class="table-container">
      <table class="table table-striped table-hover">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nom d'utilisateur</th>
            <th>Profil</th>
            <th>Filière</th>
            <th>Année Scolaire</th>
            <th>Statut</th>
            <th>Mdp par défaut</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="dataStore.isLoading && filteredUsers.length === 0">
            <td colspan="8" class="text-center">Chargement des utilisateurs...</td>
          </tr>
          <tr v-else-if="filteredUsers.length === 0">
            <td colspan="8" class="text-center">Aucun utilisateur trouvé.</td>
          </tr>
          <tr v-for="user in filteredUsers" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ getProfileName(user.profile_id) }}</td>
            <td>{{ getFiliereName(user.filiere_id) }}</td>
            <td>{{ user.annee_scolaire || 'N/A' }}</td>
            <td>
              <span :class="['badge', user.is_active ? 'bg-success' : 'bg-secondary']">
                {{ user.is_active ? 'Actif' : 'Inactif' }}
              </span>
            </td>
            <td>
              <span :class="['badge', user.is_default_password ? 'bg-warning text-dark' : 'bg-light text-secondary']">
                {{ user.is_default_password ? 'Oui' : 'Non' }}
              </span>
            </td>
            <td>
              <button @click="openEditModal(user)" class="btn btn-sm btn-warning me-2" title="Modifier">
                <span class="btn-emoji">✏️</span>
              </button>
              <button @click="toggleActivation(user)" :class="['btn btn-sm me-2', user.is_active ? 'btn-info' : 'btn-success']" :title="user.is_active ? 'Désactiver' : 'Activer'">
                <span class="btn-emoji">{{ user.is_active ? '🚫' : '✅' }}</span>
              </button>
              <button @click="confirmDelete(user.id)" class="btn btn-sm btn-danger" title="Supprimer">
                <span class="btn-emoji">🗑️</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal pour Ajout/Modification Utilisateur -->
    <div v-if="showModal" class="modal-backdrop">
      <div class="modal-content">
        <h4>{{ isEditMode ? 'Modifier l\'Utilisateur' : 'Ajouter un Utilisateur' }}</h4>
        <form @submit.prevent="handleSubmitUser">
          <div class="mb-3">
            <label for="userUsername" class="form-label">Nom d'utilisateur:</label>
            <input type="text" id="userUsername" v-model="form.username" class="form-control" required>
          </div>
          <div class="mb-3">
            <label for="userPassword" class="form-label">
              Mot de passe {{ isEditMode ? '(Laissez vide pour ne pas changer)' : '' }}:
            </label>
            <input type="password" id="userPassword" v-model="form.password" class="form-control" :required="!isEditMode">
          </div>
          <div class="mb-3">
            <label for="userProfile" class="form-label">Profil:</label>
            <select id="userProfile" v-model="form.profile_id" class="form-select" required>
              <option :value="null" disabled>Choisissez un profil</option>
              <option value="1">Admin</option>
              <option value="2">Prof</option>
              <option value="3">Étudiant</option>
            </select>
          </div>
          <div class="mb-3">
            <label for="userFiliere" class="form-label">Filière:</label>
            <select id="userFiliere" v-model="form.filiere_id" class="form-select">
              <option :value="null">Aucune (ex: pour Admin)</option>
              <option v-for="filiere in filieresForSelect" :key="filiere.id" :value="filiere.id">
                {{ filiere.nom }} {{ filiere.departement_id ? '(' + getDepartementNameForFiliere(filiere.departement_id) + ')' : '' }}
              </option>
            </select>
          </div>
          <div class="mb-3">
            <label for="userAnneeScolaire" class="form-label">Année Scolaire:</label>
            <input type="text" id="userAnneeScolaire" v-model="form.annee_scolaire" class="form-control" placeholder="Ex: 2024-2025">
          </div>
          <div class="modal-actions">
            <button type="submit" class="btn btn-success">
              <span class="btn-emoji">✔️</span>{{ isEditMode ? 'Mettre à jour' : 'Ajouter' }}
            </button>
            <button type="button" @click="closeModal" class="btn btn-secondary ms-2">
              <span class="btn-emoji">❌</span>Annuler
            </button>
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

const searchQuery = ref('');
const filterStatus = ref('');
const filterProfileId = ref('');

const filieresForSelect = computed(() => dataStore.adminFilieres);
const departementsForFiliereSelect = computed(() => dataStore.adminDepartements);

const filteredUsers = computed(() => {
  let users = dataStore.adminUsers;

  if (filterStatus.value !== '') {
    const isActiveFilter = filterStatus.value === 'true' || filterStatus.value === true;
    users = users.filter(user => user.is_active === isActiveFilter);
  }

  if (filterProfileId.value) {
    const profileId = parseInt(filterProfileId.value);
    users = users.filter(user => user.profile_id === profileId);
  }

  if (searchQuery.value.trim()) {
    const lowerSearchQuery = searchQuery.value.toLowerCase().trim();
    users = users.filter(user =>
      user.username && user.username.toLowerCase().includes(lowerSearchQuery)
    );
  }
  return users;
});

onMounted(async () => {
  if (dataStore.adminDepartements.length === 0) {
      await dataStore.fetchAdminAllDepartements();
  }
  if (dataStore.adminFilieres.length === 0) {
      await dataStore.fetchAdminAllFilieres();
  }
  await dataStore.fetchAdminAllUsers(true);
});

const getProfileName = (profileId) => {
  if (profileId === 1 || profileId === '1') return 'Admin';
  if (profileId === 2 || profileId === '2') return 'Prof';
  if (profileId === 3 || profileId === '3') return 'Étudiant';
  return 'N/A';
};

const getFiliereName = (filiereId) => {
  if (!filiereId) return 'N/A';
  const filiere = filieresForSelect.value.find(f => f.id === filiereId);
  return filiere ? filiere.nom : 'Inconnue';
};

const getDepartementNameForFiliere = (departementId) => {
  if (!departementId) return '';
  const dept = departementsForFiliereSelect.value.find(d => d.id === departementId);
  return dept ? dept.nom : 'Dept N/A';
};

const showModal = ref(false);
const isEditMode = ref(false);
const currentUserId = ref(null);

const form = reactive({
  username: '',
  password: '',
  profile_id: null,
  filiere_id: null,
  annee_scolaire: '',
});

const resetForm = () => {
  form.username = '';
  form.password = '';
  form.profile_id = null;
  form.filiere_id = null;
  form.annee_scolaire = '';
  currentUserId.value = null;
};

const openAddModal = () => {
  isEditMode.value = false;
  resetForm();
  showModal.value = true;
};

const openEditModal = (user) => {
  isEditMode.value = true;
  currentUserId.value = user.id;
  form.username = user.username;
  form.password = '';
  form.profile_id = user.profile_id;
  form.filiere_id = user.filiere_id || null;
  form.annee_scolaire = user.annee_scolaire || '';
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  resetForm();
};

const handleSubmitUser = async () => {
  if (!form.username.trim() || form.profile_id === null) {
    alert("Le nom d'utilisateur et le profil sont requis.");
    return;
  }
  if (!isEditMode.value && !form.password) {
    alert("Le mot de passe est requis pour un nouvel utilisateur.");
    return;
  }
  if ((form.profile_id === 2 || form.profile_id === 3 || form.profile_id === '2' || form.profile_id === '3') && (!form.filiere_id || !form.annee_scolaire.trim())) {
     alert("Pour les profils Professeur et Étudiant, la filière et l'année scolaire sont requises.");
     return;
  }

  try {
    const payload = {
      username: form.username,
      profile_id: parseInt(form.profile_id),
      filiere_id: form.filiere_id ? parseInt(form.filiere_id) : null,
      annee_scolaire: form.annee_scolaire.trim() || null,
    };
    if (form.password) {
      payload.password = form.password;
    }

    if (isEditMode.value && currentUserId.value) {
      await dataStore.updateUser(currentUserId.value, payload);
      alert("Utilisateur mis à jour avec succès !");
    } else {
      await dataStore.createUser(payload);
      alert("Utilisateur ajouté avec succès !");
    }
    closeModal();
  } catch (error) {
    const errorMessage = error.response?.data?.detail || error.message || "Une erreur inconnue s'est produite.";
    alert(`Erreur lors de la soumission: ${errorMessage}`);
  }
};

const confirmDelete = async (userId) => {
  if (window.confirm(`Êtes-vous sûr de vouloir supprimer cet utilisateur (ID: ${userId}) ? Cette action est irréversible.`)) {
    try {
      await dataStore.deleteUser(userId);
      alert("Utilisateur supprimé avec succès.");
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || "Une erreur inconnue s'est produite.";
      alert(`Erreur lors de la suppression: ${errorMessage}`);
    }
  }
};

const toggleActivation = async (user) => {
  const actionText = user.is_active ? "désactiver" : "activer";
  if (window.confirm(`Êtes-vous sûr de vouloir ${actionText} le compte de ${user.username} ?`)) {
    try {
      if (user.is_active) {
        await dataStore.deactivateUser(user.id);
      } else {
        await dataStore.activateUser(user.id);
      }
      alert(`Compte de ${user.username} ${!user.is_active ? 'activé' : 'désactivé'} avec succès.`);
    } catch (error) {
      const errorMessage = error.response?.data?.detail || error.message || "Une erreur inconnue s'est produite.";
      alert(`Erreur: ${errorMessage}`);
    }
  }
};
</script>

<style scoped>
.admin-users-page {
  padding: 24px;
  max-width: 1200px;
  margin: auto;
  background: #f8fafc;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(52,152,219,0.07);
}

h3 {
  color: #217dbb;
  font-size: 2em;
  margin-bottom: 18px;
  font-weight: 700;
  letter-spacing: 1px;
}

.btn {
  border-radius: 6px;
  font-weight: 600;
  font-size: 1em;
  padding: 8px 16px;
  border: none;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 0.4em;
}
.btn-primary { background: #3498db; color: #fff; }
.btn-primary:hover { background: #217dbb; }
.btn-warning { background: #f1c40f; color: #34495e; }
.btn-warning:hover { background: #ffe599; }
.btn-success { background: #27ae60; color: #fff; }
.btn-success:hover { background: #219150; }
.btn-info { background: #5bc0de; color: #fff; }
.btn-info:hover { background: #31b0d5; }
.btn-danger { background: #e74c3c; color: #fff; }
.btn-danger:hover { background: #c0392b; }
.btn-secondary { background: #95a5a6; color: #fff; }
.btn-secondary:hover { background: #7f8c8d; }
.btn-emoji { font-size: 1.1em; }

.table-container {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(52,152,219,0.07);
  overflow-x: auto;
  margin-bottom: 32px;
}

.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 1em;
}
.table th, .table td {
  padding: 0.75rem 1rem;
  text-align: left;
  vertical-align: middle;
}
.table th {
  background: #eaf2fb;
  color: #217dbb;
  font-weight: 700;
  border-bottom: 2px solid #d6eaff;
}
.table tr {
  transition: background 0.15s;
}
.table tr:hover {
  background: #f1f8ff;
}
.table td:last-child, .table th:last-child {
  text-align: center;
}

.badge {
  border-radius: 8px;
  font-size: 0.9em;
  padding: 0.4em 0.7em;
  font-weight: 600;
  display: inline-block;
}
.bg-success { background: #27ae60; color: #fff; }
.bg-secondary { background: #b2bec3; color: #fff; }
.bg-warning.text-dark { background: #ffe599; color: #b7950b !important; }
.bg-light.text-secondary { background: #f8f9fa; color: #7f8c8d; border: 1px solid #d6eaff; }

.filters-section {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(52,152,219,0.07);
  margin-bottom: 24px;
}
.filters-section .card-body {
  padding: 1.25rem;
}
.card-title {
  color: #217dbb;
  font-size: 1.2em;
  font-weight: 600;
  margin-bottom: 1rem;
}

.form-label { margin-bottom: 0.5rem; font-weight: 500; }
.form-control, .form-select {
  border-radius: 6px;
  border: 1.5px solid #d6eaff;
  background: #f8fafc;
  font-size: 1em;
  padding: 0.5em 0.9em;
  transition: border-color 0.2s;
}
.form-control:focus, .form-select:focus {
  border-color: #3498db;
  outline: none;
  background: #fff;
}

.mb-3 { margin-bottom: 1rem !important; }
.me-2 { margin-right: 0.5rem !important; }
.ms-2 { margin-left: 0.5rem !important; }
.text-center { text-align: center; }

.modal-backdrop {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(33, 125, 187, 0.18);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1050;
}
.modal-content {
  background: #fff;
  padding: 32px 28px 24px 28px;
  border-radius: 14px;
  box-shadow: 0 8px 32px rgba(52,152,219,0.13);
  width: 95%;
  max-width: 500px;
}
.modal-content h4 {
  color: #217dbb;
  font-size: 1.3em;
  margin-bottom: 18px;
  font-weight: 700;
}
.modal-actions {
  margin-top: 22px;
  text-align: right;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}
</style>
<template>
  <form @submit.prevent="submitMessage" class="chat-input-form">
    <!-- <div class="filters-container">
      <select v-model="selectedDepartement" @change="onDepartementChange" class="filter-select">
        <option :value="null">Choisir Département</option>
        <option v-for="dep in filteredDepartements" :key="dep.id" :value="dep.id">
          {{ dep.nom }}
        </option>
      </select>

      <select v-model="selectedFiliere" @change="onFiliereChange" :disabled="!selectedDepartement || dataStore.isLoading" class="filter-select">
        <option :value="null">Choisir Filière</option>
        <option v-for="fil in filieresOptions" :key="fil.id" :value="fil.id">
          {{ fil.nom }}
        </option>
      </select>

      <select v-model="selectedModule" @change="onModuleChange" :disabled="!selectedFiliere || dataStore.isLoading" class="filter-select">
        <option :value="null">Choisir Module</option>
         <option v-for="mod in modulesOptions" :key="mod.id" :value="mod.id">
          {{ mod.nom }}
        </option>
      </select>

      <select v-model="selectedActivite" :disabled="dataStore.isLoading" class="filter-select">
        <option :value="null">Choisir Activité</option>
         <option v-for="act in filteredActivites" :key="act.id" :value="act.id">
          {{ act.nom }}
        </option>
      </select>
    </div> -->
    <div class="input-area">
      <input
        type="text"
        v-model="newMessage"
        placeholder="Tapez votre message ici..."
        class="message-input"
      />
      <button type="submit" class="send-button">Envoyer</button>
    </div>
  </form>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue'; // Ajout de computed
import { useDataStore } from '@/stores/data';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const isInvite = computed(() => authStore.isInvite);

const emit = defineEmits(['send-message']);

const dataStore = useDataStore();

const newMessage = ref('');
const selectedDepartement = ref(null);
const selectedFiliere = ref(null);
const selectedModule = ref(null);
const selectedActivite = ref(null);

// Propriétés calculées pour les options des selects
// Celles-ci liront directement depuis les états du store prévus pour les dropdowns
const departementsOptions = computed(() => dataStore.departements);

const filteredDepartements = computed(() => {
  if (authStore.isInvite) {
    return departementsOptions.value.filter(dep => dep.nom === 'Scolarité')
  }
  return departementsOptions.value
})

const filieresOptions = computed(() => dataStore.filieres);
const modulesOptions = computed(() => dataStore.modules);
const activitesOptions = computed(() => dataStore.activites);

const filteredActivites = computed(() => {
  if (authStore.isInvite) {
    return activitesOptions.value.filter(act => act.nom === 'Inscription')
  }
  return activitesOptions.value
})


onMounted(async () => {
  console.log("ChatInput.vue: Component Mounted.");
  // Charger les départements initiaux si la liste est vide
  if (dataStore.departements.length === 0) {
    console.log("ChatInput.vue: Fetching departements for dropdown...");
    await dataStore.fetchDepartementsForDropdown();
  }
  // Charger les activités initiales si la liste est vide
  // (en supposant qu'elles ne dépendent pas d'une sélection précédente au montage)
  if (dataStore.activites.length === 0) {
    console.log("ChatInput.vue: Fetching activites for dropdown...");
    await dataStore.fetchActivitesForDropdown(); // <--- CORRECTION ICI
  }
});

watch(selectedDepartement, async (newDepId) => {
  console.log("ChatInput.vue: selectedDepartement changed to", newDepId);
  selectedFiliere.value = null;
  selectedModule.value = null;
  selectedActivite.value = null; // Réinitialiser aussi l'activité
  if (newDepId) {
    await dataStore.fetchFilieresByDepartement(newDepId);
  } else {
    dataStore.filieres = []; // Vider la liste des filières dans le store
    dataStore.modules = [];  // Vider aussi les modules
    // dataStore.activites = []; // Vider les activités si elles dépendent fortement du chemin
  }
});

watch(selectedFiliere, async (newFiliereId) => {
  console.log("ChatInput.vue: selectedFiliere changed to", newFiliereId);
  selectedModule.value = null;
  selectedActivite.value = null; // Réinitialiser aussi l'activité
  if (newFiliereId) {
    await dataStore.fetchModulesByFiliere(newFiliereId);
    // Si les activités dépendent directement de la filière et non du module:
    // await dataStore.fetchActivitesByFiliere(newFiliereId); // Vous auriez besoin de cette action
  } else {
    dataStore.modules = [];
    // dataStore.activites = [];
  }
});

watch(selectedModule, async (newModuleId) => {
  console.log("ChatInput.vue: selectedModule changed to", newModuleId);
  selectedActivite.value = null; // Toujours réinitialiser l'activité
  if (newModuleId) {
    // Si les activités DOIVENT être rechargées/filtrées en fonction du module:
    // 1. Assurez-vous que fetchActivitesForDropdown charge TOUTES les activités.
    // 2. Filtrez localement ou créez une action fetchActivitesByModule.
    // Pour l'instant, on suppose que dataStore.activites contient déjà ce qu'il faut
    // ou que fetchActivitesForDropdown a été appelé.
    // Si vous avez besoin de recharger spécifiquement pour ce module :
    // await dataStore.fetchActivitesByModule(newModuleId); // Vous auriez besoin de cette action
    // Si fetchActivitesForDropdown est suffisant (charge tout et vous filtrez via computed ou ici)
    // ou si les activités sont indépendantes du module une fois le module sélectionné :
    // Pas d'appel nécessaire ici si activitesOptions est déjà bien peuplé.
    // Si vous voulez forcer un rechargement de toutes les activités (moins efficace) :
    // await dataStore.fetchActivitesForDropdown();
    console.log("ChatInput.vue: Activites disponibles après sélection module:", activitesOptions.value);
  } else {
    // Si aucun module n'est sélectionné, que faire des activités ?
    // Si elles sont globales, ne rien faire. Si elles dépendent du module, les vider.
    // dataStore.activites = []; // Attention, cela affecte l'état global.
  }
});


// Les @change sur les selects ne sont plus nécessaires si les watchers font le travail.
// Si vous les gardez, assurez-vous qu'ils ne dupliquent pas la logique.
const onDepartementChange = () => { /* Logique déjà dans le watcher selectedDepartement */ };
const onFiliereChange = () => { /* Logique déjà dans le watcher selectedFiliere */ };
const onModuleChange = () => { /* Logique déjà dans le watcher selectedModule */ };


const submitMessage = () => {
  if (newMessage.value.trim() === '') return;

  const departementId = localStorage.getItem('departement_id');
  const filiereId = localStorage.getItem('filiere_id');

  const payload = {
    message: newMessage.value,
    selectedDepartement: departementId,
    selectedFiliere: filiereId,
    // selectedModule: selectedModule.value,
    // selectedActivite: selectedActivite.value,
  };

  // Log des informations avant envoi
  console.log("Envoi des données :", {
    Message: payload.message,
    Département: payload.selectedDepartement,
    Filière: payload.selectedFiliere,
    Timestamp: new Date().toISOString(),
    Source: 'submitMessage()'
  });

  emit('send-message', payload);
  newMessage.value = '';
};
</script>

<style scoped>
.chat-input-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
}

.filters-container {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.filter-select {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
  flex-grow: 1;
  min-width: 150px;
}

.filter-select:disabled {
  background-color: #e9ecef;
  cursor: not-allowed;
}

.input-area {
  display: flex;
  gap: 10px;
}

.message-input {
  flex-grow: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.send-button {
  padding: 10px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.send-button:hover {
  background-color: #0056b3;
}
</style>
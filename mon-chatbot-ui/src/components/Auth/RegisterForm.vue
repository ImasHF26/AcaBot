<template>
  <form @submit.prevent="handleRegister" class="register-form">
    <div class="form-group">
      <label for="reg-username">Nom d'utilisateur:</label>
      <input type="text" id="reg-username" v-model="username" required />
    </div>
    <div class="form-group">
      <label for="reg-password">Mot de passe:</label>
      <input type="password" id="reg-password" v-model="password" required />
    </div>
    <div class="form-group">
      <label for="profile_id"
        >ID Profil (ex: 1 pour étudiant, 2 pour enseignant):</label
      >
      <input
        type="number"
        id="profile_id"
        v-model.number="profile_id"
        required
      />
    </div>
    <div class="form-group">
      <label for="filiere_id">ID Filière (si applicable):</label>
      <input type="number" id="filiere_id" v-model.number="filiere_id" />
    </div>
    <div class="form-group">
      <label for="annee">Année (si applicable, ex: 1, 2, 3):</label>
      <input type="text" id="annee" v-model="annee" />
    </div>
    <div v-if="authStore.registerError" class="error-message">
      {{ authStore.registerError }}
    </div>
    <div v-if="authStore.registerSuccess" class="success-message">
      {{ authStore.registerSuccess }}
    </div>
    <div v-if="successMessage" class="success-message">
      {{ successMessage }}
    </div>
    <button type="submit" :disabled="authStore.isLoading">
      {{ authStore.isLoading ? "Inscription en cours..." : "S'inscrire" }}
    </button>
  </form>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const username = ref("");
const password = ref("");
const profile_id = ref(null); // ou une valeur par défaut
const filiere_id = ref(null);
const annee = ref(null);
const successMessage = ref("");

const authStore = useAuthStore();

const handleRegister = async () => {
  successMessage.value = ""; // Reset success message
  const userData = {
    username: username.value,
    password: password.value,
    profile_id: profile_id.value,
    // Envoyez null si les champs ne sont pas remplis, ou gérez la logique de validation
    filiere_id: filiere_id.value || null,
    annee: annee.value || null,
  };
  const success = await authStore.register(userData);
  if (success) {
    successMessage.value =
      "Inscription réussie ! Vous pouvez maintenant vous connecter.";
    // Optionnel: réinitialiser le formulaire
    username.value = "";
    password.value = "";
    profile_id.value = null;
    filiere_id.value = null;
    annee.value = null;
  }
};
</script>

<style scoped>
/* Réutiliser les styles de LoginForm ou créer des styles spécifiques */
.register-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}
.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}
.form-group label {
  margin-bottom: 5px;
}
.form-group input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  padding: 10px 15px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background-color: #aaa;
}
button:hover:not(:disabled) {
  background-color: #1e7e34;
}
.error-message {
  color: red;
  margin-bottom: 10px;
}
.success-message {
  color: green;
  margin-bottom: 10px;
}
</style>
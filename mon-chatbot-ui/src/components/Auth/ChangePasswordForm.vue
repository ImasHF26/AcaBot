<template>
  <form @submit.prevent="handleChangePassword" class="change-password-form">
    <div class="form-group">
      <label for="old-password">Ancien mot de passe :</label>
      <input type="password" id="old-password" v-model="oldPassword" required />
    </div>
    <div class="form-group">
      <label for="new-password">Nouveau mot de passe :</label>
      <input type="password" id="new-password" v-model="newPassword" required />
    </div>
    <div class="form-group">
      <label for="confirm-password">Confirmer le nouveau mot de passe :</label>
      <input
        type="password"
        id="confirm-password"
        v-model="confirmPassword"
        required
      />
    </div>
    <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    <div v-if="authStore.changePasswordError" class="error-message">
      {{ authStore.changePasswordError }}
    </div>
    <div v-if="authStore.changePasswordSuccess" class="success-message">
      {{ authStore.changePasswordSuccess }}
    </div>
    <button type="submit" :disabled="authStore.isLoading">
      {{
        authStore.isLoading
          ? "Modification en cours..."
          : "Changer le mot de passe"
      }}
    </button>
  </form>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const oldPassword = ref("");
const newPassword = ref("");
const confirmPassword = ref("");
const errorMessage = ref(null);
const authStore = useAuthStore();

const handleChangePassword = async () => {
  errorMessage.value = null;

  if (!oldPassword.value || !newPassword.value || !confirmPassword.value) {
    errorMessage.value = "Tous les champs sont obligatoires.";
    return;
  }

  if (newPassword.value !== confirmPassword.value) {
    errorMessage.value =
      "Le nouveau mot de passe et sa confirmation ne correspondent pas.";
    return;
  }

  await authStore.changePassword(oldPassword.value, newPassword.value);

  if (authStore.changePasswordError) {
    errorMessage.value = authStore.changePasswordError;
  } else {
    errorMessage.value = null;
  }
};
</script>

<style scoped>
.change-password-form {
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
  background-color: #ffc107;
  color: black;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background-color: #aaa;
}
button:hover:not(:disabled) {
  background-color: #e0a800;
}
.error-message {
  color: red;
  margin-bottom: 10px;
}
</style>
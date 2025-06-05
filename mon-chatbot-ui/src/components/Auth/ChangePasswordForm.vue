<template>
  <div class="change-password-card">
    <div class="change-password-header">
      <span class="change-password-icon">🔑</span>
      <h2>Changer le mot de passe</h2>
      <p class="change-password-subtitle">Sécurisez votre accès à EduLLM</p>
    </div>
    <form @submit.prevent="handleChangePassword" class="change-password-form">
      <div class="form-group">
        <label for="old-password">
          <span class="icon">🔒</span> Ancien mot de passe
        </label>
        <input type="password" id="old-password" v-model="oldPassword" required />
      </div>
      <div class="form-group">
        <label for="new-password">
          <span class="icon">🆕</span> Nouveau mot de passe
        </label>
        <input type="password" id="new-password" v-model="newPassword" required />
      </div>
      <div class="form-group">
        <label for="confirm-password">
          <span class="icon">✅</span> Confirmer le nouveau mot de passe
        </label>
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
  </div>
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
.change-password-card {
  max-width: 400px;
  margin: 60px auto 0 auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(52, 152, 219, 0.10);
  padding: 36px 32px 28px 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Segoe UI', Arial, sans-serif;
}

.change-password-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 28px;
}

.change-password-icon {
  font-size: 2.2em;
  margin-bottom: 8px;
  color: #3498db;
}

h2 {
  margin: 0 0 4px 0;
  color: #3498db;
  font-size: 1.5em;
  font-weight: 700;
  letter-spacing: 1px;
}

.change-password-subtitle {
  color: #7f8c8d;
  font-size: 1em;
  margin-bottom: 0;
  font-style: italic;
}

.change-password-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.form-group label {
  margin-bottom: 6px;
  color: #34495e;
  font-weight: 500;
  font-size: 1em;
  display: flex;
  align-items: center;
  gap: 6px;
}

.form-group input {
  padding: 11px 12px;
  border: 1.5px solid #d6eaff;
  border-radius: 6px;
  font-size: 1em;
  transition: border-color 0.2s;
  background: #f8fafc;
  color: #34495e;
}
.form-group input:focus {
  border-color: #3498db;
  outline: none;
  background: #fff;
}

button {
  padding: 12px 0;
  background-color: #f1c40f;
  color: #34495e;
  border: none;
  border-radius: 6px;
  font-size: 1.1em;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(52,152,219,0.07);
  margin-top: 8px;
  letter-spacing: 0.5px;
}
button:disabled {
  background-color: #ffe599;
  cursor: not-allowed;
}
button:hover:not(:disabled) {
  background-color: #ffd700;
}

.error-message {
  color: #c0392b;
  background: #fdecea;
  border: 1px solid #e74c3c;
  border-radius: 5px;
  padding: 8px 12px;
  font-size: 0.98em;
  margin-bottom: -10px;
  text-align: center;
}
.success-message {
  color: #27ae60;
  background: #eafaf1;
  border: 1px solid #2ecc71;
  border-radius: 5px;
  padding: 8px 12px;
  font-size: 0.98em;
  margin-bottom: -10px;
  text-align: center;
}

.icon {
  font-size: 1.1em;
  color: #f1c40f;
}
</style>
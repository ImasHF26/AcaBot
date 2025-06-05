<template>
  <div class="login-card">
    <div class="login-header">
      <img src="@/assets/logo.png" alt="EduLLM Logo" class="login-logo" />
      <h2>Connexion à EduLLM</h2>
      <p class="login-subtitle">Plateforme académique intelligente</p>
    </div>
    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="username">
          <span class="icon">👤</span> Identifiant
        </label>
        <input type="text" id="username" v-model="username" required autocomplete="username" />
      </div>
      <div class="form-group">
        <label for="password">
          <span class="icon">🔒</span> Mot de passe
        </label>
        <input type="password" id="password" v-model="password" required autocomplete="current-password" />
      </div>
      <div v-if="authStore.loginError" class="error-message">{{ authStore.loginError }}</div>
      <div v-if="authStore.loginSuccess" class="success-message">{{ authStore.loginSuccess }}</div>
      <button type="submit" :disabled="authStore.isLoading" @click="disableInviteMode">
        {{ authStore.isLoading ? "Connexion en cours..." : "Se connecter" }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const username = ref("");
const password = ref("");
const authStore = useAuthStore();

function disableInviteMode() {
  authStore.setInviteMode(false);
}

const handleLogin = async () => {
  await authStore.login({ username: username.value, password: password.value });
};
</script>

<style scoped>
/* @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&display=swap'); */

.login-card {
  max-width: 370px;
  margin: 60px auto 0 auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(52, 152, 219, 0.10);
  padding: 36px 32px 28px 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: 'Montserrat', 'Segoe UI', Arial, sans-serif;
}

.login-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 28px;
}

.login-logo {
  height: 54px;
  margin-bottom: 10px;
}

h2 {
  margin: 0 0 4px 0;
  color: #3498db;
  font-size: 1.7em;
  font-weight: 700;
  letter-spacing: 1px;
}

.login-subtitle {
  color: #7f8c8d;
  font-size: 1em;
  margin-bottom: 0;
  font-style: italic;
}

.login-form {
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
  background-color: #3498db;
  color: white;
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
  background-color: #b2dffc;
  cursor: not-allowed;
}
button:hover:not(:disabled) {
  background-color: #217dbb;
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
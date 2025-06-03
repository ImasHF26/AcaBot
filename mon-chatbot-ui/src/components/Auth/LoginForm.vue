<template>
  <form @submit.prevent="handleLogin" class="login-form" style="margin-bottom: 15px;">
    <div class="form-group">
      <label for="username">Nom d'utilisateur:</label>
      <input type="text" id="username" v-model="username" required />
    </div>
    <div class="form-group">
      <label for="password">Mot de passe:</label>
      <input type="password" id="password" v-model="password" required />
    </div>
    <!-- <div v-if="authStore.loginError" class="error-message">
      {{ authStore.loginError }}
    </div> -->

    <div v-if="authStore.loginError" class="error-message">{{ authStore.loginError }}</div>
    <div v-if="authStore.loginSuccess" class="success-message">{{ authStore.loginSuccess }}</div>

    <button type="submit" :disabled="authStore.isLoading" @click="disableInviteMode">
      {{ authStore.isLoading ? "Connexion en cours..." : "Se connecter" }}
    </button>
  </form>
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
  
  // AJOUTEZ CE LOG:
  //console.log("LoginForm.vue - Valeurs avant envoi:", {username: username.value,password: password.value,  });
  await authStore.login({ username: username.value, password: password.value });
};
</script>

<style scoped>
.login-form {
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
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
button:disabled {
  background-color: #aaa;
}
button:hover:not(:disabled) {
  background-color: #0056b3;
}
.error-message {
  color: red;
  margin-bottom: 10px;
}
</style>
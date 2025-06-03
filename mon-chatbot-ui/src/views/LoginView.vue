<template>
  <div class="login-container">
    <h2 v-if="!authStore.changePasswordRequired">Connexion</h2>
    <h2 v-else>Changement de mot de passe requis</h2>

    <LoginForm v-if="!authStore.changePasswordRequired" />
    <ChangePasswordForm v-else />

    <!-- <p v-if="!authStore.changePasswordRequired">
      Pas encore de compte? <router-link to="/register" @click="disableInviteMode">Inscrivez-vous ici</router-link>
    </p> -->
    <router-link v-if="!authStore.changePasswordRequired" to="/chat" @click="authStore.activateInviteMode()" style="color: blue; font-weight: 700;">Compte invité</router-link>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import LoginForm from '@/components/Auth/LoginForm.vue';
import ChangePasswordForm from '@/components/Auth/ChangePasswordForm.vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

function disableInviteMode() {
  authStore.setInviteMode(false);
}

const activateInviteMode = () => {
  // Configuration du mode invité
  authStore.setInviteMode(true)
  authStore.selectedDepartement = 1  // ID par défaut pour invité
  authStore.selectedFiliere = 3     // ID par défaut pour invité
  
  // Redirection vers le chat
  router.push({ name: 'Chat' })
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
  text-align: center;
}
h2 {
  margin-bottom: 20px;
}
p {
  margin-top: 20px;
}
</style>
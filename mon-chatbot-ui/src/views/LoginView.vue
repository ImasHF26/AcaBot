<template>
  <div class="login-background">
    <div class="background-overlay"></div>
    <div class="login-container">
      <h2 v-if="!authStore.changePasswordRequired">Connexion</h2>
      <h2 v-else>Changement de mot de passe requis</h2>

      <LoginForm v-if="!authStore.changePasswordRequired" />
      <ChangePasswordForm v-else />

      <!-- <p v-if="!authStore.changePasswordRequired">
        Pas encore de compte? <router-link to="/register" @click="disableInviteMode">Inscrivez-vous ici</router-link>
      </p> -->
      <span v-if="!authStore.changePasswordRequired" @click="activateInviteMode()" style="color: blue; font-weight: 700;">Compte invité</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import LoginForm from '@/components/Auth/LoginForm.vue';
import ChangePasswordForm from '@/components/Auth/ChangePasswordForm.vue';
import { useAuthStore } from '@/stores/auth';

import router from '@/router';

const authStore = useAuthStore();

function disableInviteMode() {
  authStore.setInviteMode(false);
}

const activateInviteMode = async () => {
  console.log("Activation mode invité");
  await authStore.login({ username: "Invité", password: "1" });
  // Redirection ou autres actions...
}
</script>

<style scoped>
.login-background {
  position: relative;
  min-height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  /* Background image */
  background-image: url('public/Img.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  overflow: hidden;
}

.background-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.7); /* Ajuste l’opacité selon le rendu souhaité */
  z-index: 0;
  pointer-events: none;
}

.login-container {
  position: relative;
  z-index: 1;
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
  text-align: center;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}
h2 {
  margin-bottom: 20px;
}
p {
  margin-top: 10px;
}
</style>
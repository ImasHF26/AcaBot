<template>
  <div id="app-container">
    <router-view />
  </div>
</template>

<script setup>
// Vous pouvez initialiser des choses ici si nécessaire au niveau global de l'application
import { onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

onMounted(() => {
  // Tente de charger l'utilisateur depuis le localStorage au démarrage de l'app
  // Ceci est redondant si le beforeEach du routeur le fait déjà, mais peut être utile.
  authStore.loadUserFromStorage();
});
</script>

<style>
/* Styles globaux pour #app-container si nécessaire */
#app-container {
  /* min-height: 100vh; */ /* Pour que le fond prenne toute la hauteur */
}
</style>

<!-- <script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div>
    <a href="https://vite.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div>
  <HelloWorld msg="Vite + Vue" />
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style> -->

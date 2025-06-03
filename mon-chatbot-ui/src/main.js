// src/main.js
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';
import { useAuthStore } from '@/stores/auth'; // Importez le store d'authentification
import CoreuiVue from '@coreui/vue'
import CIcon from '@coreui/icons-vue'
import '@coreui/coreui/dist/css/coreui.min.css'

const app = createApp(App);
const pinia = createPinia();

app.use(pinia); // Utilisez Pinia AVANT d'essayer d'utiliser un store

// Créez une instance du store APRÈS que Pinia soit utilisé par l'app
const authStore = useAuthStore();
authStore.loadUserFromStorage(); // Chargez l'utilisateur depuis localStorage


app.use(CoreuiVue)
app.component('CIcon', CIcon)


app.use(router);
app.mount('#app');
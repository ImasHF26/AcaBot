// src/components/Common/Navbar.vue
<template>
  <nav class="navbar">
    <div class="navbar-brand">Chatbot App</div>
    
    <!-- Liens de navigation - Masqués pour les invités -->
    <div class="navbar-links" v-if="authStore.isAuthenticated && !authStore.isInvite">
      <router-link to="/" class="nav-link">Chat</router-link>
      <router-link v-if="isAdmin || isProf" to="/ingest" class="nav-link">Ingestion</router-link>
      <router-link v-if="isAdmin || isProf" to="/documents" class="nav-link">Documents Ingérés</router-link>
      <router-link v-if="isAdmin" to="/stats" class="nav-link">Statistiques</router-link>
      <router-link v-if="isAdmin" to="/admin" class="nav-link admin-link">Administration</router-link>
    </div>

    <!-- Section utilisateur - Masquée pour les invités -->
    <div class="navbar-user" v-if="authStore.isAuthenticated && !authStore.isInvite">
      <span>Bonjour, {{ authStore.user?.username }}</span>
      <button @click="handleLogout" class="logout-button">Déconnexion</button>
    </div>

    <!-- Affichage spécifique pour les invités -->
    <div class="navbar-guest" v-if="authStore.isInvite">
      <span style="margin-right: 10px;">Mode Invité</span>
      <button @click="handleLogout" class="logout-button" style="background-color: #28a745 !important;">Connexion</button>
    </div>

    <!-- Lien de connexion - Masqué pour les invités -->
    <!-- <div class="navbar-login" v-if="!authStore.isAuthenticated && !authStore.isInvite">
      <router-link to="/login" class="nav-link login-link">Connexion</router-link>
    </div> -->
  </nav>
</template>
<script setup>
import { computed } from 'vue'; // Importez computed
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router'; // Importez useRouter pour la redirection après déconnexion

const authStore = useAuthStore();
const router = useRouter(); // Initialisez useRouter

// Propriété calculée pour vérifier si l'utilisateur est admin
// Assurez-vous que authStore.user.profile_id est bien défini après la connexion
const isAdmin = computed(() => {
  // Vérifiez d'abord si user et profile_id existent pour éviter les erreurs
  return authStore.user && authStore.user.profile_id === 1;
});
const isProf = computed(() => {
  // Vérifiez d'abord si user et profile_id existent pour éviter les erreurs
  return authStore.user && authStore.user.profile_id === 2;
});


const handleLogout = () => {
  if (authStore.isInvite) {
    // Logique spécifique pour quitter le mode invité
    authStore.isInvite = false;
    authStore.user = null;
    localStorage.removeItem('is_guest_mode');
    router.push({ name: 'Login' });
  } else {
    // Logique normale de déconnexion
    authStore.logout();
  }
};
</script>

<style scoped>
.navbar {
  background-color: #333;
  color: white;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-brand {
  font-size: 1.5em;
  font-weight: bold;
  color: #fff; /* Assurez-vous que la couleur est visible */
}

.navbar-links {
  display: flex; /* Ajout pour un meilleur alignement des liens */
  align-items: center; /* Ajout pour un meilleur alignement des liens */
}

.navbar-links .nav-link,
.navbar-login .nav-link { /* Appliquer aussi aux liens de connexion */
  color: white;
  text-decoration: none;
  margin-left: 20px;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.3s ease; /* Ajout d'une transition douce */
}

.navbar-links .nav-link:first-child {
  margin-left: 0; /* Pas de marge à gauche pour le premier lien si navbar-brand est à côté */
}


.navbar-links .nav-link:hover,
.navbar-links .router-link-exact-active, /* router-link-active peut être trop large, exact-active est mieux */
.navbar-login .nav-link:hover {
  background-color: #555;
}

.admin-link {
  /* Styles spécifiques si vous voulez que le lien admin se démarque */
  /* font-weight: bold; */
  /* color: #ffc107; */ /* Jaune pour admin par exemple */
}

.navbar-user {
  display: flex;
  align-items: center;
}

.navbar-user span {
  margin-right: 15px;
}

.logout-button {
  background-color: #d9534f;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease; /* Ajout d'une transition douce */
}

.logout-button:hover {
  background-color: #c9302c;
}

/* Styles pour le lien de connexion si l'utilisateur n'est pas authentifié */
.navbar-login .login-link {
  background-color: #5cb85c; /* Vert pour le bouton de connexion */
  padding: 8px 15px; /* Même padding que le bouton de déconnexion */
}
.navbar-login .login-link:hover {
  background-color: #4cae4c;
}
</style>
<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <div class="logo-container">
        <img src="@/assets/logo.png" alt="EduLLM Logo" class="navbar-logo" />
      </div>
      <span class="navbar-slogan">L’IA au service de l’éducation</span>
    </div>

    <!-- Liens de navigation - Masqués pour les invités -->
    <div
      class="navbar-links"
      v-if="authStore.isAuthenticated && !authStore.isInvite"
    >
      <router-link v-if="isRoleInvite" to="/" class="nav-link">Chat</router-link>
      <router-link v-if="isRoleProf" to="/ingest" class="nav-link">Ingestion</router-link>
      <router-link v-if="isRoleAdmin" to="/documents" class="nav-link">Documents Ingérés</router-link>
      <router-link v-if="isRoleAdmin" to="/stats" class="nav-link">Statistiques</router-link>
      <router-link v-if="isRoleAdmin" to="/admin" class="nav-link admin-link">Administration</router-link>
    </div>

    <!-- Section utilisateur - Masquée pour les invités -->
    <div
      class="navbar-user"
      v-if="authStore.isAuthenticated && !authStore.isInvite"
    >
      <span>Bonjour : {{ authStore.user?.username }}</span>
      <button @click="handleLogout" class="logout-button">Déconnexion</button>
    </div>

    <!-- Affichage spécifique pour les invités -->
    <div class="navbar-guest" v-if="authStore.isInvite">
      <span style="margin-right: 10px">Mode Invité</span>
      <button
        @click="handleLogout"
        class="logout-button guest"
      >
        Connexion
      </button>
    </div>

    <!-- Lien de connexion - Masqué pour les invités -->
    <div
      class="navbar-login"
      v-if="!authStore.isAuthenticated && !authStore.isInvite"
    >
      <router-link to="/login" class="nav-link login-link">Connexion</router-link>
    </div>
  </nav>
</template>

<script setup>
import { computed } from "vue";
import { useAuthStore } from "@/stores/auth";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const isRoleAdmin = computed(() => authStore.user?.profile_id === 1);
const isRoleProf = computed(() => authStore.user?.profile_id === 2 || authStore.user?.profile_id === 1);
const isRoleInvite = computed(() => authStore.user?.profile_id);

const handleLogout = () => {
  if (authStore.isInvite) {
    authStore.isInvite = false;
    authStore.user = null;
    localStorage.removeItem("is_guest_mode");
    router.push({ name: "Login" });
  } else {
    authStore.logout();
  }
};
</script>

<style scoped>
.navbar {
  background: linear-gradient(90deg, #75a4c4 0%, #74a3c3 100%);
  color: white;
  padding: 14px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-family: 'Segoe UI', Arial, sans-serif;
  box-shadow: 0 2px 12px rgba(52,152,219,0.07);
}

.logo-container {
  border: 2px solid #2d3337;
}

.navbar-brand {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 180px;
}

.navbar-logo {
  height: 70px;
  width: auto;
  margin-bottom: 2px;
  display: block;
}

.navbar-slogan {
  font-size: 0.95rem;
  color: #eaf2f8;
  margin-top: 2px;
  font-style: italic;
  letter-spacing: 0.2px;
}

.navbar-links {
  display: flex;
  align-items: center;
  gap: 12px;
}

.nav-link,
.login-link {
  color: white;
  text-decoration: none;
  margin-left: 0;
  padding: 7px 16px;
  border-radius: 5px;
  font-size: 1.08em;
  font-weight: 500;
  transition: background 0.2s, color 0.2s;
  background: transparent;
  border: none;
  outline: none;
  cursor: pointer;
}

.nav-link:hover,
.login-link:hover,
.router-link-exact-active {
  background: rgba(255,255,255,0.13);
  color: #f1c40f;
}

.admin-link {
  color: #f1c40f;
  font-weight: bold;
}

.navbar-user {
  display: flex;
  align-items: center;
  gap: 12px;
}

.navbar-user span {
  font-size: 1em;
  color: #fff;
}

.logout-button {
  background-color: #d9534f;
  color: white;
  border: none;
  padding: 8px 18px;
  border-radius: 5px;
  font-size: 1em;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
  margin-left: 8px;
}
.logout-button:hover {
  background-color: #c9302c;
}
.logout-button.guest {
  background-color: #28a745;
}
.logout-button.guest:hover {
  background-color: #218838;
}

.navbar-login .login-link {
  background-color: #f1c40f;
  color: #34495e;
  font-weight: bold;
  padding: 8px 18px;
  border-radius: 5px;
  margin-left: 0;
}
.navbar-login .login-link:hover {
  background-color: #ffe599;
  color: #217dbb;
}

@media (max-width: 900px) {
  .navbar {
    flex-direction: column;
    align-items: stretch;
    padding: 10px 8px;
    gap: 10px;
  }
  .navbar-brand {
    align-items: center;
    margin-bottom: 8px;
  }
  .navbar-links {
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
  }
  .navbar-user, .navbar-login, .navbar-guest {
    justify-content: center;
    margin-top: 8px;
  }
}
</style>
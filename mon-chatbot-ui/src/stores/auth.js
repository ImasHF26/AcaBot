import { defineStore } from 'pinia';
import api from '@/services/api';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('authToken') || null,
    loginError: null,
    loginSuccess: null,
    registerError: null,
    registerSuccess: null,
    changePasswordError: null,
    changePasswordSuccess: null,
    isLoading: false,
    isInvite: false,
    changePasswordRequired: false,
  }),
  getters: {
    isAuthenticated: (state) => !!state.user && !state.changePasswordRequired,
    currentUser: (state) => state.user,
    userId: (state) => state.user?.id,
    profileId: (state) => state.user?.profile_id,
  },
  actions: {
    setInviteMode(value) {
      this.isInvite = value;
    },

    async login(credentials) {
      this.isLoading = true;
      this.loginError = null;
      this.loginSuccess = null;
      this.changePasswordRequired = false;

      try {
        const response = await api.login(credentials);
        const data = response.data;
        console.log("Réponse du backend:", data);

        if (data.change_password_required) {
          this.user = data.user_info;
          this.changePasswordRequired = true;
          localStorage.setItem('user', JSON.stringify(this.user));
          localStorage.removeItem('authToken');
          this.loginSuccess = "Connexion réussie, veuillez changer votre mot de passe.";
        }
        else if (data.message === "Connexion réussie" && data.user_info) {
          this.user = data.user_info;

          localStorage.setItem('user_id', this.user.id);
          localStorage.setItem('profile_id', this.user.profile_id);
          localStorage.setItem('departement_id', this.user.departement_id);
          localStorage.setItem('filiere_id', this.user.filiere_id);

          const pseudoToken = btoa(JSON.stringify(this.user));
          this.token = pseudoToken;
          localStorage.setItem('authToken', pseudoToken);

          this.loginSuccess = "Connexion réussie.";
          router.push({ name: 'Chat' });
        }
        else {
          this.loginError = data.message || "Échec de la connexion.";
          this.clearAuthData();
        }
      }
      catch (error) {
        console.error("Erreur de connexion:", error);
        this.loginError = error.response?.data?.message || "Erreur serveur";
        this.clearAuthData();
      }
      finally {
        this.isLoading = false;
      }
    },
    async changePassword(oldPassword, newPassword) {
      console.log(oldPassword, newPassword);

      this.isLoading = true;
      this.changePasswordError = null;
      this.changePasswordSuccess = null;
      try {
        const response = await api.changePassword({
          user_id: this.user.id,
          old_password: oldPassword,
          new_password: newPassword,
        });
        if (response.data.message) {
          this.changePasswordRequired = false;
          this.changePasswordSuccess = response.data.message || "Mot de passe changé avec succès.";
          router.push({ name: 'Chat' });
        } else {
          this.changePasswordError = "Erreur lors du changement de mot de passe.";
        }
      } catch (error) {
        this.changePasswordError = error.response?.data?.message || error.message || "Erreur lors du changement de mot de passe.";
      } finally {
        this.isLoading = false;
      }
    },

    async register(userData) {
      this.isLoading = true;
      this.registerError = null;
      this.registerSuccess = null;
      try {
        const response = await api.register(userData);
        if (response.data.message && !response.data.message.toLowerCase().includes("erreur")) {
          this.registerSuccess = response.data.message;
          router.push({ name: 'Login' });
          return true;
        } else {
          this.registerError = response.data.message || "Échec de l'inscription.";
          return false;
        }
      } catch (error) {
        this.registerError = error.response?.data?.message || error.message || "Une erreur est survenue lors de l'inscription.";
        return false;
      } finally {
        this.isLoading = false;
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      this.loginError = null;
      this.loginSuccess = null;
      this.registerError = null;
      this.registerSuccess = null;
      this.changePasswordError = null;
      this.changePasswordSuccess = null;
      localStorage.removeItem('user');
      localStorage.removeItem('authToken');
      router.push({ name: 'Login' });
    },

    loadUserFromStorage() {
      const userString = localStorage.getItem('user');
      const tokenString = localStorage.getItem('authToken');
      if (userString) {
        this.user = JSON.parse(userString);
        if (tokenString) {
          this.token = tokenString;
        }
        this.isInvite = false;
      } else {
        this.user = null;
        this.token = null;
      }
    },
activateInviteMode() {
    // Configuration du mode invité
    this.isInvite = true;
    this.user = {
      departement_id: 1, // Département par défaut
      filiere_id: 3, // Filière par défaut
    };

    // Stockage minimal en localStorage
    localStorage.setItem('departement_id', '1');
    localStorage.setItem('filiere_id', '3');

    // Pas de token pour les invités
    localStorage.removeItem('authToken');
    this.token = null;

    // Redirection vers le chat
    router.push({ name: 'Chat' });
  },
    
  },
});
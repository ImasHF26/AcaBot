// stores/data.js
import { defineStore } from 'pinia';
import api from '@/services/api';

export const useDataStore = defineStore('data', {
  state: () => ({
    // Pour les listes déroulantes (chat, ingestion, etc.)
    departements: [],
    filieres: [], // Rempli par fetchFilieresByDepartement
    modules: [],   // Rempli par fetchModulesByFiliere
    activites: [], // Rempli par fetchActivites (si utilisé pour dropdowns)

    // Pour l'administration (listes complètes)
    adminDepartements: [],
    adminFilieres: [],
    adminModules: [],
    adminActivites: [],

    isLoading: false,
    error: null,
  }),
  actions: {
    // --- ACTIONS DE CHARGEMENT POUR LES LISTES DÉROULANTES (CHAT, INGESTION) ---
    async fetchDepartementsForDropdown() { // Renommée pour clarifier son usage
      this.isLoading = true;
      this.error = null;
      try {
        const response = await api.getDepartements();
        this.departements = response.data; // Utilisé par les dropdowns
      } catch (err) {
        this.error = "Impossible de charger les départements pour les listes déroulantes.";
        console.error("Erreur fetchDepartementsForDropdown:", err);
        this.departements = [];
      } finally {
        this.isLoading = false;
      }
    },

    async fetchFilieresByDepartement(departementId) {
      if (!departementId) {
        this.filieres = []; // Pour les dropdowns
        return;
      }
      this.isLoading = true;
      this.error = null;
      try {
        const response = await api.getFilieresByDepartement(departementId);
        this.filieres = response.data; // Pour les dropdowns
      } catch (err) {
        this.error = "Impossible de charger les filières par département.";
        console.error("Erreur fetchFilieresByDepartement:", err);
        this.filieres = [];
      } finally {
        this.isLoading = false;
      }
    },

    async fetchModulesByFiliere(filiereId) {
        if (!filiereId) {
            this.modules = []; // Pour les dropdowns
            return;
        }
        this.isLoading = true;
        this.error = null;
        try {
            const response = await api.getModulesByFiliere(filiereId);
            this.modules = response.data; // Pour les dropdowns
        } catch (err) {
            this.error = "Impossible de charger les modules par filière.";
            console.error("Erreur fetchModulesByFiliere:", err);
            this.modules = [];
        } finally {
            this.isLoading = false;
        }
    },

    async fetchActivitesForDropdown() { // Renommée pour clarifier son usage
        this.isLoading = true;
        this.error = null;
        try {
            const response = await api.getActivites();
            this.activites = response.data; // Pour les dropdowns
        } catch (err) {
            this.error = "Impossible de charger les activités pour les listes déroulantes.";
            console.error("Erreur fetchActivitesForDropdown:", err);
            this.activites = [];
        } finally {
            this.isLoading = false;
        }
    },

    // --- ACTIONS DE CHARGEMENT POUR L'ADMINISTRATION (LISTES COMPLÈTES) ---
    async fetchAdminAllDepartements(force = false) {
      if (this.adminDepartements.length > 0 && !force) return;
      this.isLoading = true;
      this.error = null;
      try {
        const response = await api.getDepartements(); // Endpoint qui retourne TOUS les départements
        this.adminDepartements = response.data;
        // Optionnel: si les dropdowns doivent aussi avoir la liste complète au démarrage
        if (this.departements.length === 0) this.departements = response.data;
      } catch (err) {
        this.error = "Impossible de charger les départements pour l'administration.";
        console.error("Erreur fetchAdminAllDepartements:", err);
        this.adminDepartements = [];
      } finally {
        this.isLoading = false;
      }
    },

    async fetchAdminAllFilieres(force = false) {
      if (this.adminFilieres.length > 0 && !force) return;
      this.isLoading = true;
      this.error = null;
      try {
        const response = await api.getFilieres(); // Endpoint qui retourne TOUTES les filières
        this.adminFilieres = response.data;
      } catch (err) {
        this.error = "Impossible de charger les filières pour l'administration.";
        console.error("Erreur fetchAdminAllFilieres:", err);
        this.adminFilieres = [];
      } finally {
        this.isLoading = false;
      }
    },

    async fetchAdminAllModules(force = false) {
      if (this.adminModules.length > 0 && !force) return;
      this.isLoading = true;
      this.error = null;
      try {
        const response = await api.getModules(); // Endpoint qui retourne TOUS les modules
        this.adminModules = response.data;
      } catch (err) {
        this.error = "Impossible de charger les modules pour l'administration.";
        console.error("Erreur fetchAdminAllModules:", err);
        this.adminModules = [];
      } finally {
        this.isLoading = false;
      }
    },

    async fetchAdminAllActivites(force = false) {
      if (this.adminActivites.length > 0 && !force) return;
      this.isLoading = true;
      this.error = null;
      try {
        const response = await api.getActivites(); // Endpoint qui retourne TOUTES les activités
        this.adminActivites = response.data;
         // Optionnel: si les dropdowns doivent aussi avoir la liste complète au démarrage
        if (this.activites.length === 0) this.activites = response.data;
      } catch (err) {
        this.error = "Impossible de charger les activités pour l'administration.";
        console.error("Erreur fetchAdminAllActivites:", err);
        this.adminActivites = [];
      } finally {
        this.isLoading = false;
      }
    },

    // --- CRUD Départements ---
    async createDepartement(data) {
      const response = await api.addDepartement(data);
      await this.fetchAdminAllDepartements(true); // Recharger la liste admin
      return response.data;
    },
    async updateDepartement(id, data) {
      const response = await api.updateDepartement(id, data);
      await this.fetchAdminAllDepartements(true);
      return response.data;
    },
    async deleteDepartement(id) {
      await api.deleteDepartement(id);
      await this.fetchAdminAllDepartements(true);
    },

    // --- CRUD Filières ---
    async createFiliere(data) {
      const response = await api.addFiliere(data);
      await this.fetchAdminAllFilieres(true); // Recharger la liste admin
      return response.data;
    },
    async updateFiliere(id, data) {
      const response = await api.updateFiliere(id, data);
      await this.fetchAdminAllFilieres(true);
      return response.data;
    },
    async deleteFiliere(id) {
      await api.deleteFiliere(id);
      await this.fetchAdminAllFilieres(true);
    },

    // --- CRUD Modules ---
    async createModule(data) {
      const response = await api.addModule(data);
      await this.fetchAdminAllModules(true); // Recharger la liste admin
      return response.data;
    },
    async updateModule(id, data) {
      const response = await api.updateModule(id, data);
      await this.fetchAdminAllModules(true);
      return response.data;
    },
    async deleteModule(id) {
      await api.deleteModule(id);
      await this.fetchAdminAllModules(true);
    },

    // --- CRUD Activités ---
    async createActivite(data) {
      const response = await api.addActivite(data);
      await this.fetchAdminAllActivites(true); // Recharger la liste admin
      return response.data;
    },
    async updateActivite(id, data) {
      const response = await api.updateActivite(id, data);
      await this.fetchAdminAllActivites(true);
      return response.data;
    },
    async deleteActivite(id) {
      await api.deleteActivite(id);
      await this.fetchAdminAllActivites(true);
    },
  },
});
// api.js (ajout des fonctions pour les utilisateurs)
import axios from 'axios';

// Configurez l'URL de base de votre API.
const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // Assurez-vous que c'est la bonne URL
  // headers: {
  //   'Content-Type': 'application/json', // Souvent géré par Axios, mais peut être utile
  // },
});

// Intercepteur pour ajouter le token d'authentification
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken'); // Ou depuis Pinia
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default {
  // Authentification
  login(credentials) {
    return apiClient.post('/login', credentials);
  },
  register(userData) {
    return apiClient.post('/register', userData);
  },
  changePassword(data) {
    return apiClient.post('/change_password', data, {
      headers: { 'Content-Type': 'application/json' }
    });
  },

  // --- Gestion des Utilisateurs (NOUVEAU) ---
  createUser(userData) { // userData: { username, email, password, full_name, role (optionnel) }
    return apiClient.post('/CreateUser/', userData);
  },
  getAllUsers() {
    return apiClient.get('/GetUsers/');
  },
  getUser(userId) {
    return apiClient.get(`/GetUser/${userId}`);
  },
  updateUser(userId, userData) { // userData: { username?, email?, full_name?, password?, role? }
    return apiClient.put(`/UpdateUser/${userId}`, userData);
  },
  deleteUser(userId) {
    return apiClient.delete(`/DelUser/${userId}`);
  },
  activateUser(userId) {
    return apiClient.patch(`/users/${userId}/activate`);
  },
  deactivateUser(userId) {
    return apiClient.patch(`/users/${userId}/deactivate`);
  },
  // --- FIN Gestion des Utilisateurs ---

  // --- Gestion des Départements ---
  getDepartements() {
    return apiClient.get('/departements');
  },
  getDepartement(id) {
    return apiClient.get(`/departements/${id}`);
  },
  addDepartement(data) {
    return apiClient.post('/departements', data);
  },
  updateDepartement(id, data) {
    return apiClient.put(`/departements/${id}`, data);
  },
  deleteDepartement(id) {
    return apiClient.delete(`/departements/${id}`);
  },

  // --- Gestion des Filières ---
  getFilieres() {
    return apiClient.get('/filieres');
  },
  getFiliere(id) {
    return apiClient.get(`/filieres/${id}`);
  },
  getFilieresByDepartement(depId) {
    return apiClient.get(`/filieresByDepartement/${depId}`);
  },
  addFiliere(data) {
    return apiClient.post('/filieres', data);
  },
  updateFiliere(id, data) {
    return apiClient.put(`/filieres/${id}`, data);
  },
  deleteFiliere(id) {
    return apiClient.delete(`/filieres/${id}`);
  },

  // --- Gestion des Modules ---
  getModules() {
    return apiClient.get('/modules');
  },
  getModule(id) {
    return apiClient.get(`/modules/${id}`);
  },
  getModulesByFiliere(filiereId) {
    return apiClient.get(`/modulesByFiliere/${filiereId}`);
  },
  addModule(data) {
    return apiClient.post('/modules', data);
  },
  updateModule(id, data) {
    return apiClient.put(`/modules/${id}`, data);
  },
  deleteModule(id) {
    return apiClient.delete(`/modules/${id}`);
  },

  // --- Gestion des Activités ---
  getActivites() {
    return apiClient.get('/activites');
  },
  getActivite(id) {
    return apiClient.get(`/activites/${id}`);
  },
  addActivite(data) {
    return apiClient.post('/activites', data);
  },
  updateActivite(id, data) {
    return apiClient.put(`/activites/${id}`, data);
  },
  deleteActivite(id) {
    return apiClient.delete(`/activites/${id}`);
  },

  // Chat
  sendMessage(chatData) {
    return apiClient.post('/chat', chatData);
  },
  getChatHistory(params) {
    return apiClient.get('/chat/history', { params });
  },

  // Ingestion
  ingestDocument(formDataPayload) {
    return apiClient.post('/ingest', formDataPayload, {
      headers: {
        'Content-Type': 'multipart/form-data',
      }
    });
  },
  getIngestedDocuments() {
    return apiClient.get('/ingested');
  },
  getStats() {
    return apiClient.get('/stats');
  },

  // Ressources (Départements, Filières, Modules, Activités)
  // getDepartements() est déjà défini plus haut
  // getFilieresByDepartement(depId) est déjà défini plus haut
  // getModulesByFiliere(filiereId) est déjà défini plus haut
  // getActivites() est déjà défini plus haut
};
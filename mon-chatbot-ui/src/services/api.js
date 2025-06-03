import axios from 'axios';


// Configurez l'URL de base de votre API.
// Assurez-vous que votre backend FastAPI est accessible à cette adresse.
const apiClient = axios.create({
  baseURL: 'http://localhost:8000', // Remplacez par l'URL de votre backend
  // headers: {
  //   'Content-Type': 'application/json',
  // },
});

// Intercepteur pour ajouter le token d'authentification (si nécessaire)
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken'); // Ou récupérez-le depuis Pinia
    if (token) {
      config.headers.Authorization = `Bearer ${token}`; // Ajustez selon votre backend
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
    //console.log('api.js service - Credentials envoyées à apiClient.post:', credentials);
    return apiClient.post('/login', credentials);
  },
  register(userData) {
    //console.log('api.js service - User data envoyées à apiClient.post:', userData);
    return apiClient.post('/register', userData);
  },

  // changePassword
  changePassword(data) {
    return apiClient.post('/change_password', data, {
      headers: { 'Content-Type': 'application/json' }
    });
  },

  // --- Gestion des Départements ---
  getDepartements() {
    return apiClient.get('/departements');
  },
  getDepartement(id) {
    return apiClient.get(`/departements/${id}`);
  },
  addDepartement(data) { // data: { nom: string }
    return apiClient.post('/departements', data);
  },
  updateDepartement(id, data) { // data: { nom: string }
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
  addFiliere(data) { // data: { nom: string, departement_id: int }
    return apiClient.post('/filieres', data);
  },
  updateFiliere(id, data) { // data: { nom: string, departement_id: int }
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
  addModule(data) { // data: { nom: string, filiere_id: int }
    return apiClient.post('/modules', data);
  },
  updateModule(id, data) { // data: { nom: string, filiere_id: int }
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
  addActivite(data) { // data: { nom: string }
    return apiClient.post('/activites', data);
  },
  updateActivite(id, data) { // data: { nom: string }
    return apiClient.put(`/activites/${id}`, data);
  },
  deleteActivite(id) {
    return apiClient.delete(`/activites/${id}`);
  },

  // Chat
  sendMessage(chatData) {
    //console.log("api.js - sendMessage - Envoi vers /chat avec payload:", chatData); // Log du payload
    //chatData: { message, departement_id, filiere_id, module_id, activite_id, profile_id, user_id }
    return apiClient.post('/chat', chatData);
  },
  getChatHistory(params) {
    //params: { profile_id, user_id, departement_id, filiere_id}
    return apiClient.get('/chat/history', { params });
  },

  // Ingestion
  ingestDocument(formDataPayload) {
    return apiClient.post('/ingest', formDataPayload, {
      headers: {
        // Forcer le Content-Type correct pour cette requête spécifique
        // Mettre 'Content-Type': undefined ou null peut aussi fonctionner pour laisser Axios le gérer
        'Content-Type': 'multipart/form-data',
      }
    });
  },
  // ingestDocument(ingestData) {
  //   // ingestData: { base_filename, file_path, departement_id, ... }
  //   // Note: Pour l'upload de fichiers, vous pourriez avoir besoin de 'multipart/form-data'
  //   // Pour l'instant, on suppose que file_path est une chaîne.
  //   // Si vous uploadez le fichier réel, la configuration d'axios sera différente.
  //   return apiClient.post('/ingest', ingestData);
  // },
  getIngestedDocuments() {
    return apiClient.get('/ingested');
  },
  getStats() {
    return apiClient.get('/stats');
  },

  // Ressources (Départements, Filières, Modules, Activités)
  getDepartements() {
    //console.log("FRONTEND (api.js): Appel de getDepartements");
    return apiClient.get('/departements');
  },
  getFilieresByDepartement(depId) {
    return apiClient.get(`/filieresByDepartement/${depId}`);
  },
  getModulesByFiliere(filiereId) {
    return apiClient.get(`/modulesByFiliere/${filiereId}`);
  },
  getActivites() { // Supposant un endpoint générique, adaptez si nécessaire
    return apiClient.get('/activites');
  },
  // Ajoutez ici les autres méthodes pour POST, PUT, DELETE des ressources si nécessaire depuis le front-end
};
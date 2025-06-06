// stores/chat.js
import { defineStore } from 'pinia';
import api from '@/services/api'; // Assurez-vous que le chemin est correct
import { useAuthStore } from '@/stores/auth'; // Assurez-vous que le chemin est correct

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [], // Pour les messages de la session de chat active
    chatHistory: [], // Pour l'historique des conversations
    isLoadingMessages: false, // Pour l'envoi de messages
    isLoadingHistory: false, // Pour le chargement de l'historique
    sendMessageError: null,
    fetchHistoryError: null, // Pour les erreurs de chargement de l'historique
  }),
  actions: {
    addMessage(message) {
      this.messages.push({ ...message, id: Date.now(), timestamp: new Date() });
    },
    async sendMessage(payload) {
      const authStore = useAuthStore();

      if (!authStore.isAuthenticated) {
        this.sendMessageError = "Utilisateur non authentifié.";
        
        console.error("sendMessage: User not authenticated or missing IDs.");
        return;
      }

      console.log("sendMessage payload:",payload);

      this.addMessage({ text: payload.message, sender: 'user' });
      this.isLoadingMessages = true;
      this.sendMessageError = null;

      console.log("Chat.js ",payload.user_id)
      const chatRequestData = {
        message: payload.message,
        departement_id: parseInt(payload.departement_id) || null,
        filiere_id: parseInt(payload.filiere_id) || null,
        module_id: parseInt(payload.module_id) || null,
        activite_id: parseInt(payload.activite_id) || null,
        profile_id: parseInt(payload.profile_id) || null,
        //user_id: parseInt(payload.userId) || null,
        show_resources: payload.show_resources || false,
        user_id: parseInt(payload.user_id) || null,
      };

      try {
        const response = await api.sendMessage(chatRequestData); // Assurez-vous que api.sendMessage existe
        this.addMessage({ text: response.data.response, sender: 'bot' });
      } catch (error) {
        const errorMessage = error.response?.data?.detail || error.message || "Erreur lors de l'envoi du message.";
        this.sendMessageError = errorMessage;
        this.addMessage({ text: `Erreur: ${errorMessage}`, sender: 'bot', isError: true });
        console.error("Erreur sendMessage:", error);
      } finally {
        this.isLoadingMessages = false;
      }
    },
    async fetchChatHistory(filters = {}) { // filters est optionnel
      const authStore = useAuthStore();

      if (!authStore.isAuthenticated || !authStore.userId || !authStore.profileId) {
        this.fetchHistoryError = "Utilisateur non authentifié pour récupérer l'historique.";
        this.chatHistory = []; // Assurer que c'est un tableau
        return;
      }

      this.isLoadingHistory = true;
      this.fetchHistoryError = null;
      try {
        const params = {
          profile_id: authStore.profileId,
          user_id: authStore.userId,
          ...filters,
        };
        // Assurez-vous que api.getChatHistory existe et est correctement configuré
        const response = await api.getChatHistory(params);
        this.chatHistory = response.data || []; // Assurer que c'est un tableau même si response.data est null/undefined
      } catch (error) {
        this.fetchHistoryError = "Impossible de charger l'historique des conversations.";
        console.error("Erreur fetchChatHistory:", error);
        this.chatHistory = []; // S'assurer que c'est un tableau en cas d'erreur
      } finally {
        this.isLoadingHistory = false;
      }
    },
    clearChat() {
        this.messages = [];
        // Peut-être aussi this.chatHistory = [] si la logique le demande lors d'un clear.
    }
  },
});
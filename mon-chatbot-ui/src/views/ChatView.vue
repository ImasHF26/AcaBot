<template>
  <div class="chat-view-container">
    <div
      style="display: flex; justify-content: space-between; align-items: center"
    >
      <h1>Chatbot</h1>
      <!-- Le lien de connexion pour invité peut rester si vous le souhaitez ici -->
      <!-- <div class="navbar-login" v-if="authStore.isInvite">
        <router-link to="/login" class="nav-link login-link">Connexion</router-link>
      </div> -->
    </div>

    <div class="chat-layout">
      <div class="chat-main">
        <ChatWindow
          :messages="chatStore.messages"
          :is-loading="chatStore.isLoadingMessages"
        />
        <ChatInput @send-message="handleSendMessage" />
        <div v-if="chatStore.sendMessageError" class="error-message">
          {{ chatStore.sendMessageError }}
        </div>
      </div>
      <!-- La section sidebar de l'historique a été supprimée d'ici -->
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from "vue"; // computed est utilisé pour isInvite
import ChatWindow from "@/components/Chat/ChatWindow.vue";
import ChatInput from "@/components/Chat/ChatInput.vue";
import { useChatStore } from "@/stores/chat";
import { useDataStore } from "@/stores/data";
import { useAuthStore } from "@/stores/auth"; // authStore est utilisé pour isInvite

const chatStore = useChatStore();
const dataStore = useDataStore();
const authStore = useAuthStore(); // Initialiser authStore

const handleSendMessage = (payload) => {
  console.log("payload",payload);
  
  console.log("chatView userId",payload.selectedUser);
  chatStore.sendMessage({
    message: payload.message,
    departement_id: payload.selectedDepartement,
    filiere_id: payload.selectedFiliere,
    show_resources: payload.showResources,
    user_id: payload.selectedUser,
    profile_id: payload.selectedProfile
  });
};
// La fonction activateInviteMode et la computed isInvite peuvent rester si le lien de connexion est ici
function activateInviteMode() { // Si vous avez besoin d'appeler cette fonction
  authStore.setInviteMode(true);
}
const isInvite = computed(() => authStore.isInvite); // Assurez-vous que isInvite existe dans authStore

// La fonction loadHistory a été supprimée d'ici


</script>

<style scoped>
/* Les styles pour .chat-sidebar, .history-list, .history-item ont été supprimés */
/* Conservez les styles pour .navbar-login si le lien de connexion reste ici */
.navbar-login .nav-link {
  color: white;
  text-decoration: none;
  margin-left: 20px;
  padding: 5px 10px;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}
.navbar-login .login-link {
  background-color: #5cb85c;
  padding: 8px 15px;
}
.navbar-login .login-link:hover {
  background-color: #4cae4c;
}

.chat-view-container {
  padding: 20px;
}
.chat-layout {
  display: flex; /* Conservez flex si vous prévoyez d'autres éléments à côté de chat-main à l'avenir */
  gap: 20px;
  margin-top: 20px;
}
.chat-main {
  flex: 1; /* Prendra toute la largeur disponible si .chat-sidebar est parti */
  display: flex;
  flex-direction: column;
}
.error-message {
  color: red;
  margin-top: 10px;
}
/* Les styles pour button (Charger l'historique) ont été supprimés */
</style>
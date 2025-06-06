<template>
  <form @submit.prevent="submitMessage" class="chat-input-form">
    <div class="input-area">
      <input
        type="text"
        v-model="newMessage"
        placeholder="Tapez votre message ici…"
        class="message-input"
        ref="textInput"
        autocomplete="off"
      />
      <v-switch
        label="Afficher les ressources"
        color="primary"
        v-model="show_resources"
      ></v-switch>
      <button
        type="button"
        @click="toggleSpeechRecognition"
        class="voice-button"
        :class="{ 'active': isListening }"
        title="Activer la reconnaissance vocale"
        aria-label="Reconnaissance vocale"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
          <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
          <line x1="12" y1="19" x2="12" y2="23"></line>
          <line x1="8" y1="23" x2="16" y2="23"></line>
        </svg>
      </button>
      <button type="submit" class="send-button">Envoyer</button>
      
    </div>
    
    <div v-if="isListening" class="speech-feedback">
      <div class="pulse-ring"></div>
      <p>🎤 En écoute… Parlez maintenant</p>
      <p class="transcript-preview">{{ interimTranscript || "Détection en cours…" }}</p>
    </div>
  </form>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, computed } from 'vue';
import { useDataStore } from '@/stores/data';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const isInvite = computed(() => authStore.isInvite);
const emit = defineEmits(['send-message']);
const dataStore = useDataStore();

const newMessage = ref('');
const textInput = ref(null);
const show_resources = ref(null);

// Reconnaissance vocale
const isListening = ref(false);
const recognition = ref(null);
const interimTranscript = ref('');
const finalTranscript = ref('');

const initSpeechRecognition = () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    console.error("Speech Recognition API non supportée dans ce navigateur");
    return;
  }
  recognition.value = new SpeechRecognition();
  recognition.value.continuous = true;
  recognition.value.interimResults = true;
  recognition.value.lang = 'fr-FR';

  recognition.value.onresult = (event) => {
    interimTranscript.value = '';
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalTranscript.value += transcript + ' ';
        newMessage.value = finalTranscript.value.trim();
      } else {
        interimTranscript.value += transcript;
      }
    }
  };

  recognition.value.onerror = (event) => {
    console.error('Erreur de reconnaissance:', event.error);
    stopRecognition();
  };

  recognition.value.onend = () => {
    if (isListening.value) {
      recognition.value.start();
    }
  };
};

const toggleSpeechRecognition = () => {
  if (isListening.value) {
    stopRecognition();
  } else {
    startRecognition();
  }
};

const startRecognition = () => {
  if (!recognition.value) {
    initSpeechRecognition();
  }
  finalTranscript.value = '';
  interimTranscript.value = '';
  isListening.value = true;
  recognition.value.start();
  textInput.value.focus();
};

const stopRecognition = () => {
  if (recognition.value) {
    recognition.value.stop();
  }
  isListening.value = false;
  if (interimTranscript.value && !finalTranscript.value) {
    newMessage.value = interimTranscript.value;
  }
};

onBeforeUnmount(() => {
  if (recognition.value) {
    recognition.value.stop();
  }
});

const submitMessage = () => {
  if (newMessage.value.trim() === '') return;
  const userid = localStorage.getItem('user_id');
  const profileid = localStorage.getItem('profile_id');
  const departementId = localStorage.getItem('departement_id');
  const filiereId = localStorage.getItem('filiere_id');
  console.log("chatInput",userid);
  const payload = {
    message: newMessage.value,
    selectedUser: userid,
    selectedProfile: profileid,
    selectedDepartement: departementId,
    selectedFiliere: filiereId,
    showResources: show_resources.value,
  };
  emit('send-message', payload);
  newMessage.value = '';
  stopRecognition();
};
</script>

<style scoped>
.chat-input-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px 14px 10px 14px;
  border: 1.5px solid #e0e0e0;
  border-radius: 12px;
  background: #f8fafc;
  box-shadow: 0 2px 8px rgba(52,152,219,0.07);
}

.input-area {
  display: flex;
  gap: 10px;
  align-items: center;
}

.message-input {
  flex-grow: 1;
  padding: 12px;
  border: 1.5px solid #d6eaff;
  border-radius: 7px;
  font-size: 1em;
  background: #fff;
  transition: border-color 0.2s;
}
.message-input:focus {
  border-color: #3498db;
  outline: none;
}

.send-button {
  padding: 11px 18px;
  background-color: #27ae60;
  color: white;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  font-size: 1em;
  font-weight: 600;
  transition: background 0.2s;
}
.send-button:hover {
  background-color: #219150;
}

.voice-button {
  padding: 10px;
  background-color: #eaf2fb;
  border: 1.5px solid #d6eaff;
  border-radius: 7px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, border-color 0.2s;
}
.voice-button:hover {
  background-color: #d6eaff;
}
.voice-button.active {
  background-color: #4CAF50;
  color: white;
  border-color: #4CAF50;
}

.speech-feedback {
  margin-top: 10px;
  padding: 12px 10px 10px 10px;
  background-color: #eaf2fb;
  border-radius: 8px;
  text-align: center;
  position: relative;
  min-height: 56px;
  box-shadow: 0 1px 4px rgba(52,152,219,0.08);
}

.pulse-ring {
  position: absolute;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 32px;
  height: 32px;
  border: 3px solid #4CAF50;
  border-radius: 50%;
  animation: pulse 1.5s infinite;
}

.transcript-preview {
  margin-top: 5px;
  font-style: italic;
  color: #217dbb;
  font-size: 1em;
}

@keyframes pulse {
  0% {
    transform: translateX(-50%) scale(0.9);
    opacity: 0.7;
  }
  70% {
    transform: translateX(-50%) scale(1.3);
    opacity: 0;
  }
  100% {
    transform: translateX(-50%) scale(0.9);
    opacity: 0;
  }
}

@media (max-width: 600px) {
  .chat-input-form {
    padding: 8px 4px 6px 4px;
    border-radius: 8px;
  }
  .input-area {
    gap: 6px;
  }
  .send-button, .voice-button {
    padding: 8px 10px;
    font-size: 0.95em;
    border-radius: 6px;
  }
  .message-input {
    padding: 8px;
    border-radius: 6px;
  }
}
</style>
<template>
  <div class="message-item" :class="{ 'user-message': isUser, 'bot-message': !isUser, 'error-message-bubble': message.isError }">
    <p class="message-text">{{ message.text }}</p>
    <span class="message-timestamp">{{ new Date(message.timestamp).toLocaleTimeString() }}</span>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  message: {
    type: Object,
    required: true, // { id, text, sender: 'user' | 'bot', timestamp, isError? }
  },
});

const isUser = computed(() => props.message.sender === 'user');
</script>

<style scoped>
.message-item {
  margin-bottom: 10px;
  padding: 10px 15px;
  border-radius: 15px;
  max-width: 70%;
  word-wrap: break-word;
}

.user-message {
  background-color: #007bff;
  color: white;
  margin-left: auto; /* Aligne à droite */
  border-bottom-right-radius: 5px;
}

.bot-message {
  background-color: #e9ecef;
  color: #333;
  margin-right: auto; /* Aligne à gauche */
  border-bottom-left-radius: 5px;
}

.error-message-bubble {
  background-color: #f8d7da;
  color: #721c24;
  border: 1px solid #f5c6cb;
}

.message-text {
  margin: 0;
  padding: 0;
}

.message-timestamp {
  display: block;
  font-size: 0.75em;
  margin-top: 5px;
  text-align: right;
  color: inherit; /* Hérite la couleur du parent pour un meilleur contraste */
  opacity: 0.8;
}

.user-message .message-timestamp {
  color: #e0e0e0;
}
.bot-message .message-timestamp {
   color: #6c757d;
}
</style>
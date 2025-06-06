<template>
  <div
    class="message-item"
    :class="{
      'user-message': isUser,
      'bot-message': !isUser,
      'error-message-bubble': message.isError
    }"
  >
    <div class="message-text" v-html="formattedText"></div>
    <span class="message-timestamp">
      {{ new Date(message.timestamp).toLocaleTimeString() }}
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { marked } from 'marked';

const props = defineProps({
  message: {
    type: Object,
    required: true, // { id, text, sender: 'user' | 'bot', timestamp, isError? }
  },
});

const isUser = computed(() => props.message.sender === 'user');

// Markdown rendering
const formattedText = computed(() => {
  // Optionnel : tu peux personnaliser marked ici si besoin
  return marked.parse(props.message.text || '');
});
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
  margin-left: auto;
  border-bottom-right-radius: 5px;
}

.bot-message {
  background-color: #e9ecef;
  color: #333;
  margin-right: auto;
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
  /* Markdown gère les retours à la ligne et la mise en forme */
}

.message-timestamp {
  display: block;
  font-size: 0.75em;
  margin-top: 5px;
  text-align: right;
  color: inherit;
  opacity: 0.8;
}

.user-message .message-timestamp {
  color: #e0e0e0;
}
.bot-message .message-timestamp {
  color: #6c757d;
}

/* Optionnel : styles pour le markdown */
.message-text h1,
.message-text h2,
.message-text h3 {
  margin: 0.5em 0 0.2em 0;
}
.message-text ul,
.message-text ol {
  margin: 0.5em 0 0.5em 1.2em;
}
.message-text code {
  background: #f4f4f4;
  padding: 2px 4px;
  border-radius: 4px;
  font-size: 0.95em;
}
.message-text pre {
  background: #f4f4f4;
  padding: 8px;
  border-radius: 6px;
  overflow-x: auto;
}
</style>
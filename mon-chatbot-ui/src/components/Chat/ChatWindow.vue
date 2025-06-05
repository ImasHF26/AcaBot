<template>
  <div class="chat-window" ref="chatWindowRef">
    <MessageItem
      v-for="msg in messages"
      :key="msg.id"
      :message="msg"
    />
    <div v-if="isLoading" class="loading-indicator">
      <div class="typing-animation" aria-label="Le bot écrit">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>
      <p>Le bot est en train d’écrire…</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue';
import MessageItem from './MessageItem.vue';

const props = defineProps({
  messages: {
    type: Array,
    required: true,
  },
  isLoading: {
    type: Boolean,
    default: false,
  }
});

const chatWindowRef = ref(null);

watch(() => props.messages, async () => {
  await nextTick();
  if (chatWindowRef.value) {
    chatWindowRef.value.scrollTop = chatWindowRef.value.scrollHeight;
  }
}, { deep: true });
</script>

<style scoped>
.chat-window {
  flex-grow: 1;
  border: 1.5px solid #e0e0e0;
  padding: 22px 18px 16px 18px;
  overflow-y: auto;
  height: 420px;
  background: linear-gradient(120deg, #f8fafc 80%, #eaf2fb 100%);
  border-radius: 16px;
  margin-bottom: 14px;
  box-shadow: 0 4px 24px rgba(52,152,219,0.07);
  scroll-behavior: smooth;
  transition: box-shadow 0.2s;
}

.chat-window:hover {
  box-shadow: 0 8px 32px rgba(52,152,219,0.13);
}

.loading-indicator {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 20px;
  background-color: #eaf2fb;
  border-radius: 18px;
  width: fit-content;
  margin: 12px 0;
  box-shadow: 0 1px 4px rgba(52,152,219,0.08);
}

.typing-animation {
  display: flex;
  align-items: center;
  height: 24px;
}

.typing-dot {
  width: 10px;
  height: 10px;
  background-color: #217dbb;
  border-radius: 50%;
  margin: 0 3px;
  animation: typingAnimation 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: 0s; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typingAnimation {
  0%, 60%, 100% {
    transform: translateY(0);
    opacity: 0.6;
  }
  30% {
    transform: translateY(-7px);
    opacity: 1;
  }
}

.loading-indicator p {
  margin: 0;
  color: #217dbb;
  font-size: 1em;
  font-style: italic;
  font-weight: 500;
  letter-spacing: 0.2px;
}

@media (max-width: 600px) {
  .chat-window {
    padding: 10px 4px 8px 4px;
    height: 320px;
    border-radius: 10px;
  }
  .loading-indicator {
    padding: 8px 10px;
    font-size: 0.95em;
  }
}
</style>
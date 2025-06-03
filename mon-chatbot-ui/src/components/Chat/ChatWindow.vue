<template>
  <div class="chat-window" ref="chatWindowRef">
    <MessageItem
      v-for="msg in messages"
      :key="msg.id"
      :message="msg"
    />
    <div v-if="isLoading" class="loading-indicator">
      <p>Le bot est en train d’écrire..</p>
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

// Auto-scroll to bottom when new messages are added
watch(() => props.messages, async () => {
  await nextTick(); // Attend que le DOM soit mis à jour
  if (chatWindowRef.value) {
    chatWindowRef.value.scrollTop = chatWindowRef.value.scrollHeight;
  }
}, { deep: true });

</script>

<style scoped>
.chat-window {
  flex-grow: 1;
  border: 1px solid #ccc;
  padding: 10px;
  overflow-y: auto;
  height: 400px; /* Hauteur fixe, ajustez si besoin */
  background-color: #f9f9f9;
  border-radius: 8px;
  margin-bottom: 10px;
}
.loading-indicator {
  text-align: center;
  padding: 10px;
  color: #777;
  font-style: italic;
}
</style>
<template>
  <div class="dashboard-layout">
    <Navbar />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import Navbar from '@/components/Common/Navbar.vue';
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  background-color: #fff; /* Ou une autre couleur de fond pour le contenu */
}
</style>
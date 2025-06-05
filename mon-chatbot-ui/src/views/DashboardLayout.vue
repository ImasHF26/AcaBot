<template>
  <div class="dashboard-layout">
    <div class="background-overlay"></div>
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
  position: relative;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  /* Background image sur le layout principal */
  background-image: url('public/Img.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
}

.background-overlay {
  position: absolute;
  inset: 0;
  background: rgba(255, 255, 255, 0.7); /* Blanc semi-transparent, ajuste l’opacité ici */
  z-index: 0;
  pointer-events: none; /* Pour ne pas gêner les interactions */
}

.main-content {
  flex-grow: 1;
  padding: 20px;
  position: relative;
  z-index: 1; /* Pour que le contenu soit au-dessus de l’overlay */
  /* Pas besoin de background ici, il hérite du layout */
}
</style>
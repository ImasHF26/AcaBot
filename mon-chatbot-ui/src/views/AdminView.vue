// src/views/AdminView.vue
<template>
  <div class="admin-view">
    <h2>Administration</h2>
    <nav class="admin-nav">
      <router-link to="/admin/register">Inscription</router-link>
      <router-link to="/admin/departements">Départements</router-link>
      <router-link to="/admin/filieres">Filières</router-link>
      <router-link to="/admin/modules">Modules</router-link>
      <router-link to="/admin/activites">Activités</router-link>
    </nav>
    <div class="admin-content">
      <router-view></router-view> <!-- Les composants enfants s'afficheront ici -->
    </div>
  </div>
</template>

<script setup>
// Pas de script spécifique nécessaire pour ce layout simple
</script>

<style scoped>
.admin-view {
  padding: 20px;
}
.admin-nav {
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}
.admin-nav a {
  margin-right: 15px;
  text-decoration: none;
  color: #007bff;
  font-weight: 500;
}
.admin-nav a.router-link-exact-active {
  color: #0056b3;
  border-bottom: 2px solid #0056b3;
}
.admin-content {
  margin-top: 20px;
}
</style>
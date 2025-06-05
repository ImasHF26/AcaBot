<!-- src/views/NonAutorisePage.vue -->
<template>
  <div class="non-autorise-container">
    <div class="icon-container">
      <!-- Vous pouvez utiliser une icône SVG ou une image ici -->
      <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-slash">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="4.93" y1="4.93" x2="19.07" y2="19.07"></line>
      </svg>
    </div>
    <h1>Accès Non Autorisé</h1>
    <p>
      Vous n'avez pas les permissions nécessaires pour accéder à cette page.
    </p>
    <p>
      Si vous pensez qu'il s'agit d'une erreur, veuillez contacter l'administrateur du site.
    </p>
    <router-link to="/" class="bouton-retour">Retour à l'accueil</router-link>
  </div>
</template>

<script>
export default {
  name: 'NonAutorisePage'
};
</script>

<style scoped>
.non-autorise-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 80vh; /* Ajustez selon la hauteur de votre layout */
  text-align: center;
  padding: 20px;
  font-family: Arial, sans-serif;
  color: #333;
}

.icon-container {
  margin-bottom: 20px;
  color: #e74c3c; /* Rouge pour l'erreur/interdiction */
}

.icon-container svg {
  width: 80px;
  height: 80px;
}

h1 {
  font-size: 2.5em;
  color: #c0392b; /* Rouge plus foncé */
  margin-bottom: 10px;
}

p {
  font-size: 1.1em;
  line-height: 1.6;
  margin-bottom: 15px;
  max-width: 500px;
}

.bouton-retour {
  display: inline-block;
  padding: 10px 20px;
  margin-top: 20px;
  background-color: #3498db; /* Bleu pour l'action principale */
  color: white;
  text-decoration: none;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.bouton-retour:hover {
  background-color: #2980b9;
}
</style>
<template>
  <div class="register-container">
    <h2>Inscription</h2>
    <RegisterForm />
     <!-- <p>Déjà un compte? <router-link to="/login">Connectez-vous ici</router-link></p> -->
  </div>
</template>

<script setup>
import RegisterForm from '@/components/Auth/RegisterForm.vue';
</script>

<style scoped>
.register-container {
  max-width: 100%;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
  text-align: center;
}
h2 {
  margin-bottom: 20px;
}
p {
  margin-top: 20px;
}
</style>
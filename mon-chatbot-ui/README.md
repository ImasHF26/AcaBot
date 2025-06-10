# EduLLMBot FrontEnd

Ce projet est une interface web développée avec Vue 3 et Vite pour le chatbot éducatif EduLLMBot.

## Prérequis
- Node.js (version recommandée : >=16)
- npm ou yarn

## Installation
1. Clonez le dépôt :
   ```bash
   git clone <url-du-repo>
   cd FrontEnd
   ```
2. Installez les dépendances :
   ```bash
   npm install
   # ou
   yarn install
   ```

## Lancement du projet en développement
```bash
npm run dev
# ou
yarn dev
```
Le projet sera accessible sur `http://localhost:5173` (par défaut).

## Tâches principales du projet
- **Développement de l'interface utilisateur** :
  - Utilisation de Vue 3 avec `<script setup>`
  - Composants modulaires (authentification, chat, administration, ingestion, statistiques...)
- **Gestion de l'authentification** :
  - Connexion, inscription, changement de mot de passe
- **Gestion des chats** :
  - Envoi et affichage des messages
- **Administration** :
  - Gestion des départements, filières, modules, activités
- **Ingestion de documents** :
  - Formulaire d'import de documents
- **Visualisation de statistiques** :
  - Graphiques (BarChart, PieChart)
- **Navigation** :
  - Navbar, routing avec Vue Router
- **Gestion d'état** :
  - Utilisation de Pinia (stores)
- **Tests** :
  - (À compléter selon la stack de test utilisée)
- **Build pour la production** :
  ```bash
  npm run build
  # ou
  yarn build
  ```
  Les fichiers générés seront dans le dossier `dist/`.

## Structure du projet
- `src/components/` : Composants Vue (auth, chat, admin, etc.)
- `src/views/` : Pages principales
- `src/router/` : Configuration du routing
- `src/services/` : Appels API
- `src/stores/` : Stores Pinia
- `public/` : Fichiers statiques



## Liens utiles
- [Documentation Vue 3](https://vuejs.org/)
- [Documentation Vite](https://vitejs.dev/)
- [Pinia (gestion d'état)](https://pinia.vuejs.org/)

---
N'hésitez pas à ouvrir une issue pour toute question ou suggestion !

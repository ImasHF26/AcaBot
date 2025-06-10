# 🤖 EduLLM Chatbot

Bienvenue dans **EduLLM Chatbot** ! Ce chatbot Python fonctionne localement, s’appuie sur l’API Ollama Local (`http://localhost:11434/api/generate`) et le modèle multimodal **gemma3:4b** pour offrir une assistance académique rapide, fiable et hors-ligne.

---

## 🌟 Fonctionnalités

- **🏡 Exécution Locale**  
  Tout se passe sur votre machine : aucune connexion internet ou API externe requise, garantissant confidentialité et accès ininterrompu.

- **🤖 Chat IA**  
  Profitez de réponses intelligentes, contextuelles et adaptées à vos besoins éducatifs.

- **💻 Génération de Contenu**  
  Créez des cours complets, des quiz stimulants et des résumés concis de documents pédagogiques.

- **⚡ Léger et Rapide**  
  Utilise le modèle efficace **gemma3:4b** pour des performances optimales sans compromis sur la qualité.

- **🧠 RAG Avancé (Retrieval-Augmented Generation)**  
  - **Embedding** : Intégration avec `BAAI/bge-base-en-v1.5` pour des embeddings robustes et une compréhension sémantique précise.  
  - **Découpage & Recouvrement** : Découpe intelligente des documents en segments avec recouvrement pour préserver le contexte.  
  - **Base de Vecteurs** : Utilisation de **FaissDB** pour un stockage et une recherche rapide des informations pertinentes.  
  - **Similarité Cosinus** : Recherche des informations les plus proches sémantiquement.  
  - **Reranking** : Raffinement des résultats pour ne garder que les plus pertinents et cohérents.  
  - **Génération de Réponse** : Synthèse claire, concise et précise à partir des segments retrouvés.

- **🚀 Backend FastAPI**  
  Construit avec **FastAPI** pour une API robuste, performante et facile à utiliser.

---

## 📋 Prise en Main

Suivez ces étapes pour installer et lancer le chatbot :

### 1️⃣ Cloner le Dépôt

```bash
git clone https://github.com/ImasHF26/EduLLM.git
cd EduLLM
```

### 2️⃣ Installer les dépendances
Assurez-vous d’avoir Python 3.11 ou plus. Créez un environnement virtuel et installez les dépendances :

```bash
python -m venv .venv
.venv\Scripts\activate  # Sur Windows
pip install -r requirements.txt
```

### 3️⃣ Vérifier que l’API locale fonctionne 🖥️
Le chatbot s’appuie sur une API locale pour générer les réponses. Vérifiez que l’API Ollama fonctionne à l’adresse http://localhost:11434/api/generate.

Modèle utilisé : gemma3:4b  
Pourquoi ce modèle ? Il offre un bon compromis entre performance, rapidité et précision, idéal pour des conversations éducatives et la génération de contenu.

Si l’API n’est pas démarrée, référez-vous à la documentation officielle d’Ollama pour configurer le serveur local et télécharger le modèle gemma3:4b.

### 4️⃣ Lancer le chatbot 🚀
Une fois les dépendances installées et l’API locale démarrée, lancez le chatbot :

```bash
uvicorn api.main:app --reload
```

Ouvrez votre navigateur et rendez-vous à l’adresse indiquée par Uvicorn (généralement http://127.0.0.1:8000).

### 💬 Exemples d’utilisation
Commencez à discuter ! Par exemple, vous pouvez demander :

- "Qu'est ce qu'un perceptron ?"
- "Donne-moi une introduction au DevOps."
- "Crée un quiz sur l'apprentissage automatique."
- "Résume le concept de la régression linéaire."

---

## 📌 Tâches principales du projet

- Installation et configuration de l’environnement Python et des dépendances
- Mise en place et vérification de l’API Ollama et du modèle gemma3:4b
- Lancement du backend FastAPI
- Développement et maintenance des fonctionnalités principales (chat, génération de contenu, RAG, etc.)
- Tests et validation du fonctionnement du chatbot
- Documentation et amélioration continue

---

## 🤝 Contribution
Les contributions sont les bienvenues ! 🛠️

Si vous souhaitez contribuer, veuillez forker le dépôt, créer une branche pour vos fonctionnalités ou corrections, puis soumettre une pull request. Merci d’aider à améliorer EduLLM !
from typing import Optional, Dict, Any, List

class PromptBuilder:

    @staticmethod
    def is_qcm_request(user_query: str) -> bool:
        qcm_keywords = [
            "qcm", "quiz", "question à choix multiple", "questions à choix multiples", "choix multiple"
        ]
        return any(keyword.lower() in user_query.lower() for keyword in qcm_keywords)

    @staticmethod
    def build_standard_prompt(context_text, user_query):
        return (
            f"# Contexte\n"
            f"{context_text}\n\n"
            f"# Question\n"
            f"{user_query}\n\n"
            "Vous êtes un assistant pédagogique. Réponds uniquement à partir du contexte fourni ci-dessus, sans ajouter, inférer ni reformuler d’informations extérieures.\n"
            "Le cadre est académique : adopte un ton engageant et motivant pour l’étudiant, tout en restant clair, précis et inspirant.\n"
            "Fournis une explication concise et une justification, sans introduction ou répétition superflue.\n"
            "Supprime toute balise <...> dans la réponse.\n"
            "Exprime-toi uniquement en français.\n"
            "Formate toute la réponse en **Markdown** selon la charte suivante :\n\n"
            "---\n"
            "## ✨ Réponse\n"
            "> [Une phrase claire, précise et inspirante, directement issue du contexte.]\n"
            "---\n"
            "## 📚 Ressources supplémentaires (si disponibles)\n"
            "- [Titre de la ressource 1](URL)\n"
            "- [Titre de la ressource 2](URL)\n"
            "---\n"
            "- N’affiche la section « Ressources supplémentaires » que si des ressources pertinentes sont disponibles.\n"
            "- Ne fournis jamais d’informations non présentes dans le contexte.\n"
            "- Ne réponds pas si le contexte est vide ou ne contient pas d’informations pertinentes pour la question.\n"
            "- Ne réponds pas si la question est hors sujet ou ne peut pas être traitée avec les informations fournies.\n"
            "- Ne réponds pas si la question est trop vague ou nécessite des informations supplémentaires pour être traitée.\n"
            "- Ne réponds pas si la question est une demande de QCM, utilise plutôt la méthode `build_qcm_prompt`.\n"
            "- Ne réponds pas si la question est une demande de résumé, utilise plutôt la méthode `build_summary_prompt`.\n"
            
        )

    @staticmethod
    def build_qcm_prompt(context_text, user_query, max_questions=20):
        return (
            f"# Contexte\n"
            f"{context_text}\n\n"
            f"# Question\n"
            f"{user_query}\n\n"
            "En te basant uniquement sur le contexte fourni, génère un QCM lié à la question ci-dessus.\n"
            f"Génère jusqu'à {max_questions} questions, chacune avec 4 propositions, et indique clairement la bonne réponse.\n"
            "Formate le QCM en **Markdown** selon l'exemple ci-dessous :\n\n"
            "---\n"
            "### Question 1\n"
            "1. Choix A\n"
            "2. Choix B\n"
            "3. Choix C\n"
            "4. Choix D\n"
            "**Réponse correcte :** 2\n"
            "---\n"
            "Exprime-toi uniquement en français.\n"
            "Ne fournis jamais d’informations non présentes dans le contexte.\n"
            
        )

    @staticmethod
    def build_summary_prompt(context_text, user_query):
        return (
            f"# Contexte\n"
            f"{context_text}\n\n"
            f"# Demande\n"
            f"{user_query}\n\n"
            "En te basant uniquement sur le contexte fourni, rédige un résumé clair, concis et structuré des informations essentielles.\n"
            "N'ajoute aucune information extérieure, ne reformule pas ce qui n'est pas dans le contexte.\n"
            "Exprime-toi uniquement en français.\n"
            "Formate le résumé en **Markdown** selon la charte suivante :\n\n"
            "---\n"
            "## 📝 Résumé\n"
            "> [Un résumé synthétique, fidèle au contexte, sans ajout ni interprétation.]\n"
            "---\n"
            "- Ne réponds pas si le contexte est vide ou ne contient pas d'informations pertinentes pour la demande.\n"
            "- Ne réponds pas si la question est hors sujet ou ne peut pas être traitée avec les informations fournies.\n"
            "- Ne réponds pas si la question est trop vague ou nécessite des informations supplémentaires pour être traitée.\n"
            "- Ne réponds pas si la question est une demande de QCM, utilise plutôt la méthode `build_qcm_prompt`.\n"
            "- Ne réponds pas si la question est une demande de réponse standard, utilise plutôt la méthode `build_standard_prompt`.\n"
           
        )
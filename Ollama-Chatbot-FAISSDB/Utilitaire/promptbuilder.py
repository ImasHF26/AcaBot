from typing import Optional, Dict, Any, List

class PromptBuilder:

    def is_qcm_request(user_query: str) -> bool:
        qcm_keywords = [
            "qcm", "quiz", "question à choix multiple", "questions à choix multiples", "choix multiple"
        ]
        return any(keyword.lower() in user_query.lower() for keyword in qcm_keywords)

    
    def build_standard_prompt(context_text, user_query):
        return (
            f"Contexte :\n{context_text}\n\n"
            f"Question : {user_query}\n\n"
            "Vous êtes un assistant pédagogique. Réponds uniquement à partir du contexte fourni ci-dessus, sans ajouter, inférer ni reformuler d’informations extérieures.\n"
            "Le cadre est académique : adopte un ton engageant et motivant pour l’étudiant, tout en restant clair, précis et inspirant.\n"
            "Fournis une explication concise, sans introduction, justification ou répétition superflue.\n"
            "Supprime toute balise <...> dans la réponse.\n"
            "Exprime-toi uniquement en français.\n"
            "Respecte strictement le format ci-dessous :\n"
            "********************\n"
            "Réponse :\n"
            "[Une phrase claire, précise et inspirante, directement issue du contexte.]\n"
            "********************\n"
            "Ressources supplémentaires (si disponibles) :\n"
            "- [Titre de la ressource 1] : [URL]\n"
            "- [Titre de la ressource 2] : [URL]\n"
            "********************\n"
            "N’affiche la section « Ressources supplémentaires » que si des ressources pertinentes sont disponibles.\n"
            "Ne fournis jamais d’informations non présentes dans le contexte.\n"
        )

   
    def build_qcm_prompt(context_text, user_query, max_questions=10):
        return (
            f"Contexte :\n{context_text}\n\n"
            f"Question : {user_query}\n\n"
            "En te basant uniquement sur le contexte fourni, génère un QCM lié à la question ci-dessus.\n"
            f"Génère jusqu'à {max_questions} questions, chacune avec 4 propositions, et indique clairement la bonne réponse.\n"
            "Format :\n"
            "Question : [ta question]\n"
            "1) choix A\n"
            "2) choix B\n"
            "3) choix C\n"
            "4) choix D\n"
            "Réponse correcte : [numéro ou texte]\n"
            "Exprime-toi uniquement en français.\n"
            "Ne fournis jamais d’informations non présentes dans le contexte.\n"
        )
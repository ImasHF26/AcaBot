import os
from ollama_api import OllamaAPI
from rag_chatbot import RAGChatbot

def main():
    ollama_api = OllamaAPI()
    chatbot = RAGChatbot(ollama_api)

    print("Bienvenue dans le système RAG !")
    print("Commandes disponibles :")
    print("- 'Ingestion chemin_du_fichier' : pour Ingester un fichier (txt, pdf, docx, json)")
    print("- 'chat' : pour démarrer une conversation")
    print("- 'exit' : pour quitter")

    while True:
        command = input("\nEntrez une commande : ").strip()

        if command.lower() == "exit":
            print("Au revoir !")
            break
        elif command.lower() == "chat":
            try :
                print("=== Configuration du contexte académique ===")
                departement_id = int(input("ID du département : "))
                filiere_id = int(input("ID de la filière : "))
                module_id = int(input("ID du module : "))
                activite_id = int(input("ID de l'activité : "))
                profile_id = int(input("ID du profil (1=Admin, 2=Prof, 3=Etudiant, 4=Invité) : "))
                user_id = int(input("Votre identifiant utilisateur : "))
                print("Contexte enregistré.\n")

                chatbot.chat(
                    departement_id=departement_id,
                    filiere_id=filiere_id,
                    module_id=module_id,
                    activite_id=activite_id,
                    profile_id=profile_id,
                    user_id=user_id
                )

            except ValueError:
                print("Erreur : tous les identifiants doivent être des entiers valides.")   
        elif command.lower().startswith("index "):
            file_path = command[6:].strip()
            base_filename = os.path.basename(file_path)
            #print(base_filename)
            if not os.path.exists(file_path):
                print(f"Le fichier {file_path} n'existe pas ou n'est pas accessible.")
                continue
            
            try:
                
                # Demander à l'utilisateur les métadonnées nécessaires
                departement_id = int(input("ID du département : "))
                filiere_id = int(input("ID de la filière : "))
                module_id = int(input("ID du module : "))
                activite_id = int(input("ID de l'activité (1=Inscription, 2=Cours, 3=TD, 4=TP...) : "))
                profile_id = int(input("ID du profil (1=Admin, 2=Prof, 3=Etudiant, 4=Invité) : "))
                user_id = int(input("ID de l'utilisateur (par exemple 1 pour admin test) : "))

                # Appel de la méthode avec tous les paramètres
                chatbot.ingestion_file(
                    base_filename,
                    file_path,
                    departement_id=departement_id,
                    filiere_id=filiere_id,
                    module_id=module_id,
                    activite_id=activite_id,
                    profile_id=profile_id,
                    user_id=user_id
                )

            except ValueError:
                print("Erreur : tous les identifiants doivent être des entiers valides.")
            except Exception as e:
                print(f"Une erreur est survenue lors de l'indexation : {e}")
        else:
            print("Commande non reconnue. Veuillez réessayer.")

if __name__ == "__main__":
    main()
import sys
import time
import os, re
import pickle
import faiss
import numpy as np
from colorama import Fore, Style
from sentence_transformers import SentenceTransformer
# Supposons que OllamaAPI, FileProcessor, FilterManager sont correctement importés
from ollama_api import OllamaAPI
from Utilitaire.file_processor import FileProcessor
from Utilitaire.filter_manager import FilterManager
import traceback # Pour un meilleur débogage

class RAGChatbot:
    def __init__(self, ollama_api, chunk_size=384, chunk_overlap=96, faiss_index_file='./vector_store/faiss_index.faiss', metadata_file='./vector_store/metadata.pickle', hashes_file='./vector_store/hashes.pickle'):
        self.ollama_api = ollama_api
        self.embedding_model = SentenceTransformer('BAAI/bge-base-en-v1.5')
        self.file_processor = FileProcessor(chunk_size, chunk_overlap)
        self.dimension = 768  # Correct pour BAAI/bge-base-en-v1.5
        self.MCNoeud = 32
        self.efSearch = 200
        self.efConstruction = 128
        self.faiss_index_file = faiss_index_file
        self.metadata_file = metadata_file
        self.hashes_file = hashes_file

        self.index = self.load_or_initialize_index()
        self.metadata = self.load_or_initialize_metadata() # C'est une liste de dictionnaires
        self.load_processed_hashes()

    def normalize_embedding(self, embedding):
        norm = np.linalg.norm(embedding)
        return embedding / norm if norm > 0 else embedding

    def load_or_initialize_index(self):
        if os.path.exists(self.faiss_index_file):
            # print(f"Chargement de l'index Faiss depuis {self.faiss_index_file}")
            return faiss.read_index(self.faiss_index_file)
        else:
            print("Initialisation d'un nouvel index Faiss HNSWFlat.")
            # Pour IndexHNSWFlat, le deuxième argument est M (nombre de connexions)
            # La métrique par défaut pour IndexHNSWFlat est L2.
            # Si vous voulez utiliser le produit scalaire (IP) pour la similarité cosinus
            # après normalisation, l'index plat sous-jacent doit être IP.
            # IndexHNSWFlat stocke les vecteurs dans un IndexFlatL2 par défaut.
            # Pour utiliser IP avec HNSW, vous pouvez utiliser faiss.IndexHNSWSQ ou construire
            # un IndexHNSW sur un IndexFlatIP.
            # Cependant, IndexHNSWFlat avec METRIC_INNER_PRODUCT est aussi une option.
            # index = faiss.IndexHNSWFlat(self.dimension, self.MCNoeud) # Utilise L2 par défaut
            index = faiss.IndexHNSWFlat(self.dimension, self.MCNoeud, faiss.METRIC_INNER_PRODUCT)
            index.hnsw.efSearch = self.efSearch
            index.hnsw.efConstruction = self.efConstruction
            return index

    def load_or_initialize_metadata(self):
        if os.path.exists(self.metadata_file):
            #print(f"Chargement des métadonnées depuis {self.metadata_file}")
            with open(self.metadata_file, 'rb') as f:
                return pickle.load(f)
        else:
            print("Initialisation d'une nouvelle liste de métadonnées.")
            return []

    def load_processed_hashes(self):
        if os.path.exists(self.hashes_file):
            #print(f"Chargement des hashes traités depuis {self.hashes_file}")
            with open(self.hashes_file, 'rb') as f:
                self.file_processor.processed_hashes = pickle.load(f)
        else:
            #print("Initialisation d'un nouvel ensemble de hashes traités.")
            # Assurez-vous que processed_hashes est initialisé dans FileProcessor si le fichier n'existe pas
            if not hasattr(self.file_processor, 'processed_hashes'):
                 self.file_processor.processed_hashes = set()


    def save_state(self):
        print("Sauvegarde de l'état (index, métadonnées, hashes)...")
        os.makedirs(os.path.dirname(self.faiss_index_file), exist_ok=True)
        faiss.write_index(self.index, self.faiss_index_file)
        with open(self.metadata_file, 'wb') as f:
            pickle.dump(self.metadata, f)
        with open(self.hashes_file, 'wb') as f:
            pickle.dump(self.file_processor.processed_hashes, f)
        print("État sauvegardé.")

    def ingestion_file(self, base_filename, file_content, departement_id, filiere_id, module_id, activite_id, profile_id, user_id):
        try:
            chunks, file_hash = self.file_processor.process_file(base_filename, file_content)
            if chunks is None:
                print(f"Traitement de {base_filename} annulé (déjà traité ou contenu non valide).")
                if file_hash:
                    raise ValueError(f"Le fichier {base_filename} (hash: {file_hash}) a déjà été traité.")
                else:
                    raise ValueError(f"Le contenu du fichier {base_filename} n'a pas pu être traité ou était vide.")
            if not chunks:
                print(f"Aucun chunk extrait de {base_filename}. L'indexation est annulée pour ce fichier.")
                return

            embeddings = []
            for chunk_text_content in chunks:
                # Pour BGE, il est recommandé de ne pas ajouter d'instruction aux documents lors de l'indexation.
                embedding = self.embedding_model.encode([chunk_text_content], normalize_embeddings=True)[0]
                # La normalisation est déjà faite par normalize_embeddings=True
                # normalized_embedding = self.normalize_embedding(embedding) # Plus besoin si normalize_embeddings=True
                embeddings.append(embedding) # Utiliser directement l'embedding normalisé

            if not embeddings:
                print(f"Aucun embedding n'a pu être généré pour les chunks de {base_filename}.")
                raise ValueError(f"Échec de la génération d'embeddings pour {base_filename}.")

            embeddings_np = np.array(embeddings, dtype='float32')
            start_index = self.index.ntotal
            self.index.add(embeddings_np)

            for i, chunk_text_content in enumerate(chunks):
                current_global_chunk_index = start_index + i
                self.metadata.append({
                    "file_hash": file_hash,
                    "original_filename": base_filename,
                    "faiss_index": current_global_chunk_index,
                    "chunk_text": chunk_text_content,
                    # Stocker aussi les filtres pour un accès direct si nécessaire, ou compter sur la DB
                    "departement_id": departement_id,
                    "filiere_id": filiere_id,
                    "module_id": module_id,
                    "activite_id": activite_id,
                    "profile_id": profile_id,
                    "user_id": user_id
                })
                FilterManager.insert_metadata_sqlite(
                    base_filename=base_filename, file_hash=file_hash,
                    chunk_index=current_global_chunk_index, chunk_text=chunk_text_content,
                    departement_id=departement_id, filiere_id=filiere_id, module_id=module_id,
                    activite_id=activite_id, profile_id=profile_id, user_id=user_id
                )
            self.save_state()
            print(f"Fichier {base_filename} indexé. {len(chunks)} chunks ajoutés. L'index Faiss contient maintenant {self.index.ntotal} vecteurs.")
        except ValueError as ve:
            print(f"Erreur de valeur lors de l'indexation de {base_filename} : {str(ve)}")
            raise
        except Exception as e:
            print(f"Erreur inattendue lors de l'indexation de {base_filename} : {str(e)}")
            traceback.print_exc()
            raise

    def find_relevant_context(self, user_query,
                              departement_id=None, filiere_id=None,
                              top_k=3, similarity_threshold=0.65):
        """
        Recherche les chunks les plus pertinents pour une requête utilisateur,
        en utilisant les ID Faiss globaux filtrés et en reconstruisant les vecteurs correctement.
        """
        try:
            # Pour BGE, il est souvent recommandé d'ajouter une instruction aux requêtes.
            # Consultez la documentation du modèle BGE spécifique.
            # Pour 'BAAI/bge-base-en-v1.5', l'instruction est souvent:
            # "Represent this sentence for searching relevant passages: "
            # Cependant, SentenceTransformer peut le gérer implicitement pour certains modèles.
            # Si vous utilisez normalize_embeddings=True, la normalisation est déjà faite.
            query_embedding = self.embedding_model.encode([user_query], normalize_embeddings=True)[0]
            # normalized_query = self.normalize_embedding(query_embedding).reshape(1, -1) # Plus besoin
            normalized_query = query_embedding.reshape(1, -1)
        except Exception as e:
            print(f"Erreur lors de la génération de l'embedding de la requête: {e}")
            traceback.print_exc()
            return None

        if not hasattr(self.index, 'ntotal') or self.index.ntotal == 0:
            print("Aucun contexte indexé dans Faiss ou l'index n'est pas correctement initialisé.")
            return None

        try:
            allowed_faiss_ids = FilterManager.get_allowed_indices(
                departement_id, filiere_id
            )
        except Exception as e:
            print(f"Erreur lors de la récupération des IDs autorisés depuis FilterManager: {e}")
            traceback.print_exc()
            return None

        if not allowed_faiss_ids:
            print("Aucun chunk autorisé trouvé pour ce contexte académique et ces filtres.")
            return None

        allowed_faiss_ids_array = np.array(list(allowed_faiss_ids), dtype='int64')
        valid_ids_for_reconstruction = np.array(
            [fid for fid in allowed_faiss_ids_array if 0 <= fid < self.index.ntotal],
            dtype='int64'
        )

        if len(valid_ids_for_reconstruction) == 0:
            print("Aucun ID Faiss autorisé n'est actuellement valide dans l'index principal.")
            return None

        sub_vectors_list = []
        try:
            # Pour IndexHNSWFlat, les vecteurs sont dans 'storage' qui est un IndexFlat.
            # Si self.index.storage n'existe pas ou est None, il y a un problème avec l'init de l'index HNSW.
            if not hasattr(self.index, 'storage') or self.index.storage is None:
                 print("L'index HNSW ne semble pas avoir de 'storage' valide pour la reconstruction.")
                 return None
            
            reconstruction_source = self.index.storage
            for vector_id in valid_ids_for_reconstruction:
                reconstructed_vec = reconstruction_source.reconstruct(int(vector_id))
                sub_vectors_list.append(reconstructed_vec)

            if not sub_vectors_list:
                print("La liste des vecteurs reconstruits est vide.")
                return None
            sub_vectors = np.array(sub_vectors_list, dtype='float32')

        except AttributeError as ae:
            print(f"Erreur d'attribut lors de la reconstruction (vérifiez type d'index): {ae}")
            traceback.print_exc()
            return None
        except Exception as e:
            print(f"Erreur inattendue lors de la reconstruction des vecteurs: {e}")
            traceback.print_exc()
            return None

        if sub_vectors.shape[0] == 0:
            print("Aucun vecteur n'a pu être reconstruit (shape[0] est 0).")
            return None

        try:
            # Le sous-index doit utiliser la même métrique que l'index principal si on compare les scores
            # Si l'index HNSW utilise METRIC_INNER_PRODUCT, le sous-index aussi.
            sub_index = faiss.IndexFlatIP(self.dimension)
            sub_index.add(sub_vectors)
        except Exception as e:
            print(f"Erreur lors de la création/ajout au sous-index Faiss: {e}")
            traceback.print_exc()
            return None

        try:
            k_search = min(top_k, sub_index.ntotal)
            if k_search == 0:
                print("Le sous-index est vide, impossible de rechercher.")
                return None
            distances, local_indices_in_sub = sub_index.search(normalized_query, k_search)
        except Exception as e:
            print(f"Erreur lors de la recherche sur le sous-index Faiss: {e}")
            traceback.print_exc()
            return None

        relevant_chunks_texts = []
        # print(f"Debug: Distances brut: {distances}")
        # print(f"Debug: Indices locaux brut: {local_indices_in_sub}")

        for i, distance_val in zip(local_indices_in_sub[0], distances[0]):
            print(f"Debug: Indice local: {i}, Distance: {distance_val:.4f}")
            # Vérifier si l'indice est valide
            if i >= 0 and distance_val >= similarity_threshold: # Pour IP, distance plus élevée = plus similaire
                global_faiss_id = valid_ids_for_reconstruction[i]
                
                # Récupérer le texte du chunk à partir de self.metadata (liste de dictionnaires)
                chunk_data = None
                for meta_item in self.metadata: # Itération pour trouver le bon item
                    if meta_item.get("faiss_index") == global_faiss_id:
                        chunk_data = meta_item
                        break
                
                if chunk_data and 'chunk_text' in chunk_data:
                    relevant_chunks_texts.append(chunk_data['chunk_text'])
                    print(f"Debug: Chunk pertinent trouvé: ID={global_faiss_id}, Similarité={distance_val:.4f}")
                else:
                    print(f"Attention : Métadonnées ou texte du chunk introuvables pour l'ID Faiss global {global_faiss_id}")
            # else:
                # print(f"Debug: Chunk écarté: Index local={i}, Similarité={distance_val:.4f}, Seuil={similarity_threshold}")


        if not relevant_chunks_texts:
            print("Aucun chunk pertinent trouvé (seuil de similarité non atteint ou problème de métadonnées).")
            return None
        
        return relevant_chunks_texts

    # ... (autres méthodes : clean_llm_response, generate_response, etc. restent inchangées) ...
    def clean_llm_response(self, response: str) -> str:
    # Extraire uniquement le texte après la dernière occurrence de '</'
        if '</' in response:
            response = response.split('</')[-1]

        # Nettoyage supplémentaire
        cleaned = re.sub(r"<?think>", "", response, flags=re.DOTALL | re.IGNORECASE)
        cleaned = re.sub(r"</?think>", "", cleaned, flags=re.IGNORECASE)
        return cleaned.strip()

    def generate_response(self, user_query, departement_id, filiere_id):
        # Appelle votre méthode pour trouver le contexte pertinent
        context_chunks = self.find_relevant_context(
            user_query, departement_id, filiere_id, top_k=3, similarity_threshold=0.55
        )

        prompt_text = "" # Initialise la variable pour le texte de l'invite

        if context_chunks:  # Si context_chunks n'est pas None et n'est pas une liste vide
            context_text_joined = "\n".join(context_chunks)
            prompt_text = (
                f"Contexte :\n{context_text_joined}\n\n"
                f"Question : {user_query}\n"
                "Répondre uniquement sur la base du contexte fourni ci-dessus, sans ajouter, inférer ni reformuler d'informations extérieures. "
                "Le cadre est strictement académique. Fournir une réponse directe, concise, sans introduction, justification ni énumération. "
                "Supprimer toute réponse contenant ou entourée par des balises <...>.., comme celle du raisonnement. Répondre uniquement en français. "
                "Ne pas ajouter d'introduction, de justification, d'énumération ou toute autre information."
                "Ne répète pas l'information." # Suggestion d'ajustement    
                "La réponse doit se limiter à une phrase claire et exacte.\n\n"
                "Réponse :"
            )
        else:
            # Ceci est l'invite de votre bloc 'else' original
            prompt_text = (
                f"Question : {user_query}\n"
                "Répondre uniquement sur la base du contexte fourni ci-dessus..." # Note ci-dessous
                "Sans ajouter, inférer ni reformuler d'informations extérieures au contexte implicite de la question. " # Suggestion d'ajustement
                "Le cadre est strictement académique. Fournir une réponse directe, concise, sans introduction, justification ni énumération. "
                "Supprimer toute réponse contenant ou entourée par des balises  <...>.., comme celle du raisonnement. Répondre uniquement en français. "
                "Ne pas ajouter d'introduction, de justification, d'énumération ou toute autre information."
                "La réponse doit se limiter à une phrase claire et exacte.\n\nRéponse :"
            )
        
        llm_raw_response = self.ollama_api.chat_with_ollama(prompt_text)
        cleaned_llm_response = self.clean_llm_response(llm_raw_response)

        # FilterManager.save_chat_history(
        #     user_id=user_id, question=user_query, answer=cleaned_llm_response,
        #     departement_id=departement_id, filiere_id=filiere_id, module_id=module_id,
        #     activite_id=activite_id, profile_id=profile_id
        #)
        return cleaned_llm_response

    def simulate_typing(self, text, delay=0.009):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def format_response(self, response):
        formatted_response = ""
        for char in response:
            if char.isdigit():
                formatted_response += Fore.BLUE + char + Style.RESET_ALL
            elif char == '`':
                formatted_response += Fore.GREEN + char + Style.RESET_ALL
            else:
                formatted_response += char
        return formatted_response

    def display_welcome_message(self):
        welcome_message = Fore.GREEN + "Chatbot: Bonjour ! Tapez 'exit' pour quitter." + Style.RESET_ALL
        self.simulate_typing(welcome_message)

    def display_exit_message(self):
        exit_message = Fore.RED + "Chatbot: Au revoir ! À bientôt !" + Style.RESET_ALL
        self.simulate_typing(exit_message)

    def chat(self, departement_id, filiere_id, module_id, activite_id, profile_id, user_id):
        self.display_welcome_message()
        while True:
            user_input = input("\n" + Fore.YELLOW + "Vous : " + Style.RESET_ALL)
            if user_input.lower() == "exit":
                self.display_exit_message()
                break
            try:
                response = self.generate_response(user_input, departement_id, filiere_id, module_id, activite_id, profile_id, user_id)
                formatted_response = self.format_response(response)
                self.simulate_typing(Fore.CYAN + f"Chatbot : {formatted_response}" + Style.RESET_ALL)
            except Exception as e:
                self.simulate_typing(Fore.RED + f"Chatbot : Désolé, une erreur s'est produite : {str(e)}" + Style.RESET_ALL)
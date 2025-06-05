import sqlite3
import hashlib
from typing import Optional, Dict, Any, List
import api.models as models
# from api.models.exceptions import UserNotFoundError, DuplicateUserError, ChatHistoryEntry

class UserNotFoundError(Exception):
    pass

class DuplicateUserError(Exception):
    pass
from datetime import date, timedelta


# Database path
db_path = "./bdd/chatbot_metadata.db"

class FilterManager:

    def __init__(self, db_path: str):
        self.db_path = db_path

    def hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate(self, username: str, password: str) -> Optional[dict]:
        print("Authentification user:", username)
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.password, u.profile_id,d.id as departement_id, u.filiere_id, u.annee_scolaire, u.is_active, u.is_default_password
            FROM users u, departements d, filieres f
            where u.filiere_id = f.id
            and f.departement_id= d.id
            and u.username = ?
        """, (username,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None  # Utilisateur non trouvé

        if row["is_active"] != 1:
            return {"error": "Utilisateur inactif."}

        if row["password"] != self.hash_password(password):
            return {"error": "Username ou mot de passe incorrect."}

        # Authentification réussie
        user_data = {
            "id": row["id"],
            "username": username,
            "profile_id": row["profile_id"],
            "filiere_id": row["filiere_id"],
            "annee_scolaire": row["annee_scolaire"],
            "departement_id": row["departement_id"],  # Added
            "is_active": bool(row["is_active"])
        }

        if row["is_default_password"] == 1:
            user_data["change_password_required"] = True

        return user_data

    # User registration
    # --- Opérations CRUD ---

    class UserNotFoundError(Exception):
        pass

    class DuplicateUserError(Exception):
        pass

    def get_db_connection(self):
        """Crée et retourne une connexion à la base de données."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row # Pour accéder aux colonnes par nom
        return conn

    # def get_user_by_id(self, user_id):
    #     """Récupère un utilisateur par son ID."""
    #     conn = self.get_db_connection()
    #     cursor = conn.cursor()
    #     cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    #     user = cursor.fetchone()
    #     conn.close()
    #     if user:
    #         return dict(user) 
    #     return None

    def _db_row_to_user_response_dict(self, row: sqlite3.Row) -> Optional[Dict[str, Any]]:
        if not row:
            return None
        user_dict = dict(row)
        # Convertir les booléens stockés en INTEGER en bool Python
        user_dict['is_active'] = bool(user_dict.get('is_active', 0))
        user_dict['is_default_password'] = bool(user_dict.get('is_default_password', 0))
        return user_dict

    def create_user(self, user_data: models.UserCreate) -> Dict[str, Any]:
        hashed_password = self.hash_password(user_data.password)
        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, password, profile_id, filiere_id, annee_scolaire, is_active, is_default_password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_data.username, hashed_password, user_data.profile_id,
                  user_data.filiere_id, user_data.annee_scolaire,
                  int(user_data.is_active), int(user_data.is_default_password)))
            conn.commit()
            user_id = cursor.lastrowid
            # Récupérer l'utilisateur créé pour le retourner
            created_user_row = cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            return self._db_row_to_user_response_dict(created_user_row)
        except sqlite3.IntegrityError:
            raise DuplicateUserError(f"Le nom d'utilisateur '{user_data.username}' existe déjà.")
        finally:
            conn.close()

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user_row = cursor.fetchone()
        conn.close()
        return self._db_row_to_user_response_dict(user_row)

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user_row = cursor.fetchone()
        conn.close()
        return self._db_row_to_user_response_dict(user_row)

    def get_all_users(self) -> List[Dict[str, Any]]:
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users')
        users_rows = cursor.fetchall()
        conn.close()
        return [self._db_row_to_user_response_dict(row) for row in users_rows if row]

    def update_user(self, user_id: int, user_data: models.UserUpdate) -> Optional[Dict[str, Any]]:
        current_user = self.get_user_by_id(user_id)
        if not current_user:
            raise UserNotFoundError(f"Utilisateur avec ID {user_id} non trouvé.")

        update_fields = {}
        if user_data.username is not None:
            update_fields['username'] = user_data.username
        if user_data.password is not None: # Si un nouveau mot de passe est fourni
            update_fields['password'] = self.hash_password(user_data.password)
        if user_data.profile_id is not None:
            update_fields['profile_id'] = user_data.profile_id
        if user_data.filiere_id is not None:
            update_fields['filiere_id'] = user_data.filiere_id
        if user_data.annee_scolaire is not None: # Note: alias 'annee' géré par Pydantic
            update_fields['annee_scolaire'] = user_data.annee_scolaire
        if user_data.is_active is not None:
            update_fields['is_active'] = int(user_data.is_active)
        if user_data.is_default_password is not None:
            update_fields['is_default_password'] = int(user_data.is_default_password)

        if not update_fields:
            return current_user # Rien à mettre à jour

        set_clause = ", ".join([f"{key} = ?" for key in update_fields.keys()])
        values = list(update_fields.values())
        values.append(user_id)

        conn = self.get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(f"UPDATE users SET {set_clause} WHERE id = ?", tuple(values))
            conn.commit()
            if cursor.rowcount == 0: # Au cas où, bien que vérifié avant
                raise UserNotFoundError(f"Utilisateur avec ID {user_id} non trouvé lors de la tentative de mise à jour.")
            return self.get_user_by_id(user_id) # Retourner l'utilisateur mis à jour
        except sqlite3.IntegrityError: # Ex: si on essaie de changer username pour un existant
            raise DuplicateUserError(f"Conflit de données lors de la mise à jour, potentiellement un nom d'utilisateur dupliqué.")
        finally:
            conn.close()

    def delete_user(self, user_id: int) -> bool:
        conn = self.get_db_connection()
        cursor = conn.cursor()
        # Vérifier d'abord si l'utilisateur existe
        user = self.get_user_by_id(user_id)
        if not user:
            conn.close()
            raise UserNotFoundError(f"Utilisateur avec ID {user_id} non trouvé.")
        
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        deleted_count = cursor.rowcount
        conn.close()
        return deleted_count > 0

    def set_user_active_status(self, user_id: int, active_status: bool) -> Optional[Dict[str, Any]]:
        return self.update_user(user_id, models.UserUpdate(is_active=active_status))

    # def get_user_by_id(self, user_id: int):
    #     conn = self.get_db_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    #     user = cursor.fetchone()
    #     conn.close()
    #     return user

    def change_password(self, user_id: int, new_password: str) -> str:
        try:
            hashed_password = self.hash_password(new_password)
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute("""
                    UPDATE users
                    SET password = ?, is_default_password = 0
                    WHERE id = ?
                """, (hashed_password, user_id))
                if c.rowcount == 0:
                    raise ValueError("Utilisateur non trouvé ou mise à jour impossible.")
                conn.commit()
            return "Mot de passe changé avec succès."
        except Exception as e:
            # Vous pouvez logger l'erreur ici si besoin
            raise RuntimeError(f"Erreur lors du changement de mot de passe : {str(e)}")
        
    # Traçabilité des conversations par utilisateur
    def save_chat_history( user_id, question, answer, departement_id, filiere_id, profile_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO chat_history (user_id, question, answer, departement_id, filiere_id, profile_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, question, answer, departement_id, filiere_id, profile_id))

        conn.commit()
        conn.close()
    # Inserer les metadonnées des docs ds BDD chatbot_metadata
    
    def insert_metadata_sqlite(base_filename, file_hash, chunk_index, chunk_text, departement_id, filiere_id, module_id, activite_id, profile_id, user_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO document_metadata (base_filename, file_hash, chunk_index, chunk_text, departement_id, filiere_id, module_id, activite_id, profile_id, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (base_filename, file_hash, chunk_index, chunk_text, departement_id, filiere_id, module_id, activite_id, profile_id, user_id))
        conn.commit()
        conn.close()


    @staticmethod
    def get_allowed_indices(departement_id=None, filiere_id=None):
        """
        Retourne un ensemble d'ID Faiss (chunk_index globaux stockés dans la DB)
        autorisés en fonction des filtres académiques.
        """
        # print(">>> Filtres reçus dans get_allowed_indices :")
        # print(f"  departement_id={departement_id}")
        # print(f"  filiere_id={filiere_id}")
        # print(f"  module_id={module_id}")
        # print(f"  activite_id={activite_id}")
        # print(f"  profile_id={profile_id}")
        # print(f"  user_id={user_id}")

        conn = sqlite3.connect(db_path) # Assurez-vous que db_path est défini
        cursor = conn.cursor()

        # Construire la requête SQL de base
        query_parts = ["SELECT chunk_index FROM document_metadata WHERE 1=1"]
        params = []

        # Ajouter des conditions pour chaque filtre s'il est fourni
        if departement_id is not None:
            query_parts.append("AND departement_id = ?")
            params.append(departement_id)
        if filiere_id is not None:
            query_parts.append("AND filiere_id = ?")
            params.append(filiere_id)
       

        final_query = " ".join(query_parts)
        # print(f"Executing SQL: {final_query} with params: {params}")

        cursor.execute(final_query, tuple(params))

        # chunk_index dans la base de données EST maintenant l'ID global Faiss.
        # Nous récupérons donc directement ces IDs.
        allowed_faiss_ids = set(row[0] for row in cursor.fetchall())

        conn.close()

        # print(f"Allowed FAISS IDs from DB: {allowed_faiss_ids}")
        return allowed_faiss_ids
    
    def get_documents_ingested(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT DISTINCT dm.base_filename, dm.file_hash, dm.chunk_text, dm.user_id , u.username, dm.date_Ingestion,
                d.nom, f.nom, m.nom, a.nom, p.nom
            FROM document_metadata dm
            LEFT JOIN departements d ON dm.departement_id = d.id
            LEFT JOIN filieres f ON dm.filiere_id = f.id
            LEFT JOIN modules m ON dm.module_id = m.id
            LEFT JOIN activites a ON dm.activite_id = a.id
            LEFT JOIN profile p ON dm.profile_id = p.id
            LEFT JOIN users u ON dm.user_id = u.id
            WHERE dm.file_hash IS NOT NULL
            ORDER BY dm.file_hash, dm.chunk_index
        """)

        rows = cursor.fetchall()
        conn.close()

        # On regroupe les chunks par fichier
        documents = {}
        for row in rows:
            base_filename,file_hash, chunk_text, user_id, username, date_Ingestion, dep, fil, mod, act, prof = row
            if file_hash not in documents:
                documents[file_hash] = {
                    "base_filename" : base_filename,
                    "file_hash" : file_hash,
                    "user_id" : user_id,
                    "username" : username,
                    "date_Ingestion" : date_Ingestion,
                    "departement": dep,
                    "filiere": fil,
                    "module": mod,
                    "activite": act,
                    "profile": prof,
                    "chunks": []
                }
            documents[file_hash]["chunks"].append(chunk_text)

        # Ajouter taille et nb chunks
        result = []
        for doc in documents.values():
            result.append({
                **doc,
                "nb_chunks": len(doc["chunks"]),
                "taille_estimee": round(sum(len(c) for c in doc["chunks"])/1024 ,2)
            })

        return result
    
    def get_ingestion_statistics(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        stats = {}

        # Total de documents (distincts par file_hash)
        cursor.execute("SELECT COUNT(DISTINCT file_hash) FROM document_metadata")
        stats["total_documents"] = cursor.fetchone()[0]

        # Statistiques temporelles (supposant une colonne 'date_ingestion' TEXT au format YYYY-MM-DD HH:MM:SS)
        today_str = date.today().isoformat()
        start_of_week_str = (date.today() - timedelta(days=date.today().weekday())).isoformat()
        start_of_month_str = date.today().replace(day=1).isoformat()

        cursor.execute("SELECT COUNT(DISTINCT file_hash) FROM document_metadata WHERE date(date_ingestion) = ?", (today_str,))
        stats["ingested_today"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT file_hash) FROM document_metadata WHERE date(date_ingestion) >= ?", (start_of_week_str,))
        stats["ingested_this_week"] = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(DISTINCT file_hash) FROM document_metadata WHERE date(date_ingestion) >= ?", (start_of_month_str,))
        stats["ingested_this_month"] = cursor.fetchone()[0]

        # Répartition par département
        cursor.execute("""
            SELECT d.nom, COUNT(DISTINCT dm.file_hash)
            FROM document_metadata dm
            JOIN departements d ON dm.departement_id = d.id
            GROUP BY d.nom
        """)
        stats["documents_par_departement"] = [{"departement": row[0], "count": row[1]} for row in cursor.fetchall()]

        # Répartition par filière
        cursor.execute("""
            SELECT f.nom, COUNT(DISTINCT dm.file_hash)
            FROM document_metadata dm
            JOIN filieres f ON dm.filiere_id = f.id
            GROUP BY f.nom
        """)
        stats["documents_par_filiere"] = [{"filiere": row[0], "count": row[1]} for row in cursor.fetchall()]

        # Répartition par module
        cursor.execute("""
            SELECT m.nom, COUNT(DISTINCT dm.file_hash)
            FROM document_metadata dm
            JOIN modules m ON dm.module_id = m.id
            GROUP BY m.nom
        """)
        stats["documents_par_module"] = [{"module": row[0], "count": row[1]} for row in cursor.fetchall()]

        # Répartition par activité
        cursor.execute("""
            SELECT a.nom, COUNT(DISTINCT dm.file_hash)
            FROM document_metadata dm
            JOIN activites a ON dm.activite_id = a.id
            GROUP BY a.nom
        """)
        stats["documents_par_activite"] = [{"activite": row[0], "count": row[1]} for row in cursor.fetchall()]

        conn.close()
        return stats
    
    def get_chat_history(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
            SELECT 
                p.nom AS profile, 
                u.username, 
                dep.nom AS departement, 
                f.nom AS filiere,
                ch.question, 
                ch.answer, 
                ch.timestamp
            FROM chat_history ch
            JOIN profile p ON ch.profile_id = p.id
            JOIN users u ON ch.user_id = u.id
            JOIN departements dep ON ch.departement_id = dep.id
            JOIN filieres f ON ch.filiere_id = f.id
            
            ORDER BY ch.timestamp DESC
        """

        #print("Query: ", query)
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        return [
            models.ChatHistoryEntry(
                profile=row[0],
                username=row[1],
                departement=row[2],
                filiere=row[3],
                user_query=row[4],
                chatbot_response=row[5],
                timestamp=row[6]
            )
            for row in rows
        ]
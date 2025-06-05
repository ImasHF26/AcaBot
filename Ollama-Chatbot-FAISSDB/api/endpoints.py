from fastapi import APIRouter, HTTPException, Query , Depends,Form, UploadFile, File, status, Body
from rag_chatbot import RAGChatbot
from ollama_api import OllamaAPI
from .models import *
import api.models as models
from Utilitaire.ResourceManager import ResourceManager
from fastapi.responses import JSONResponse
import sqlite3
from typing import List, Dict, Optional
from Utilitaire.filter_manager import FilterManager
from RessourceSuppl.RS_Models import Resource, ResourceCreate, ResourceOut
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

db_path = "./bdd/chatbot_metadata.db"

# SQLAlchemy engine and session setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./bdd/chatbot_metadata.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter()
ollama_api = OllamaAPI()
chatbot = RAGChatbot(ollama_api)
filter_manager = FilterManager(db_path)
manager = ResourceManager()

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ENDPOINTS PRINCIPAUX
@router.post("/login", response_model=models.LoginResponse) 
def login(data: models.LoginRequest):
    user_info = filter_manager.authenticate(data.username, data.password)
    if not user_info:
        raise HTTPException(status_code=401, detail="Nom d'utilisateur ou mot de passe incorrect")

    if "error" in user_info:
        # Utilisateur inactif ou autre erreur détectée dans authenticate
        raise HTTPException(status_code=401, detail=user_info["error"])

    if user_info.get("change_password_required"):
        return {
            "message": "Changement de mot de passe requis",
            "change_password_required": True,
            "user_info": user_info
        }

    return {
        "message": "Connexion réussie",
        "user_info": user_info
    }


# --- Endpoints CRUD plus génériques ---

# @router.post("/users/", response_model=models.UserResponse, status_code=status.HTTP_201_CREATED)
# def create_new_user(user_data: models.UserCreate):
#     try:
#         created_user = filter_manager.create_user(user_data)
#         return created_user
#     except filter_manager.DuplicateUserError as e:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# Endpoint d'enregistrement Users

@router.post("/CreateUser/", response_model=models.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user_endpoint(data: models.UserCreate):
    try:
        created_user = filter_manager.create_user(data)
        return created_user
    except filter_manager.DuplicateUserError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur interne du serveur: {str(e)}")


@router.get("/GetUser/{user_id}", response_model=models.UserResponse)
def read_user(user_id: int):
    user = filter_manager.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Utilisateur non trouvé")
    return user

@router.get("/GetUsers/", response_model=List[models.UserResponse])
def read_all_users():
    users = filter_manager.get_all_users()
    return users

@router.put("/UpdateUser/{user_id}", response_model=models.UserResponse)
def update_existing_user(user_id: int, user_update_data: models.UserUpdate):
    try:
        updated_user = filter_manager.update_user(user_id, user_update_data)
        return updated_user
    except filter_manager.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except filter_manager.DuplicateUserError as e: # Si la mise à jour cause un username dupliqué
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/DelUser/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_user(user_id: int):
    try:
        if not filter_manager.delete_user(user_id):
            # Normalement, delete_user lève UserNotFoundError si non trouvé
            pass # La fonction delete_user lève une exception si non trouvé
    except filter_manager.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return None # Réponse 204 No Content

# --- Endpoints d'activation/désactivation ---

@router.patch("/users/{user_id}/activate", response_model=models.UserResponse)
def activate_user_endpoint(user_id: int):
    try:
        user = filter_manager.set_user_active_status(user_id, True)
        return user
    except filter_manager.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.patch("/users/{user_id}/deactivate", response_model=models.UserResponse)
def deactivate_user_endpoint(user_id: int):
    try:
        user = filter_manager.set_user_active_status(user_id, False)
        return user
    except filter_manager.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# @router.post("/register")
# def register_user(data: RegisterRequest):
#     try:
#         result = filter_manager.register_user(
#             username=data.username,
#             password=data.password,
#             profile_id=data.profile_id,
#             filiere_id=data.filiere_id,
#             annee=data.annee
#         )
#         if "Erreur" in result:
#             raise HTTPException(status_code=400, detail=result)
#         return {"message": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/change_password")
def change_password(data: ChangePasswordRequest):
    try:
        user = filter_manager.get_user_by_id(data.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

        # Vérifier l'ancien mot de passe
        if user["password"] != filter_manager.hash_password(data.old_password):
            raise HTTPException(status_code=400, detail="Ancien mot de passe incorrect")

        result = filter_manager.change_password(data.user_id, data.new_password)
        if "Erreur" in result:
            raise HTTPException(status_code=400, detail=result)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat", response_model=ChatResponse)
def chat_with_context(data: ChatRequest, db: Session = Depends(get_db)):
    result = chatbot.generate_response(
        user_query=data.message,
        user_id=data.user_id,
        profile_id=data.profile_id,
        departement_id=data.departement_id,
        filiere_id=data.filiere_id
    )
    resources = []
    if getattr(data, "show_resources", False):
        context_tags = Resource.extract_tags_from_question(data.message)
        resources = Resource.get_additional_resources(db, context_tags)
    return {
        "response": result,
        "resources": [ResourceOut.from_orm(r) for r in resources]
    }

# @router.post("/chat", response_model=ChatResponse)
# def chat_with_context(data: ChatRequest):
#     result = chatbot.generate_response(
#         user_query=data.message,
#         user_id=data.user_id,
#         profile_id=data.profile_id,
#         departement_id=data.departement_id,
#         filiere_id=data.filiere_id
#     )
#     return {"response": result}

# @router.post("/ingest")
# def ingest_document(data: IngestRequest):
#     try:
#         chatbot.ingestion_file(
#             base_filename = data.base_filename,
#             file_path=data.file_path,
#             departement_id=data.departement_id,
#             filiere_id=data.filiere_id,
#             module_id=data.module_id,
#             activite_id=data.activite_id,
#             profile_id=data.profile_id,
#             user_id=data.user_id,
#         )
#         return {"status": "success", "message": f"{data.file_path} indexé avec succès."}
#     except Exception as e:
#         return {"status": "error", "message": str(e)}

@router.post("/ingest")
async def ingest_document_endpoint( # Renommé pour éviter confusion avec la méthode de la classe
    # Champs Form pour les métadonnées
    base_filename: str = Form(...),
    departement_id: int = Form(...),
    profile_id: int = Form(...),
    user_id: int = Form(...),
    filiere_id: Optional[int] = Form(None),
    module_id: Optional[int] = Form(None),
    activite_id: Optional[int] = Form(None),
    # Le fichier uploadé
    file_upload: UploadFile = File(...)  # Le fichier est maintenant requis
):
    try:
        # chatbot est une instance de votre classe Chatbot, assurez-vous qu'elle est accessible ici
        # Par exemple, via une dépendance, ou si elle est initialisée globalement (moins idéal pour les tests)
        # from main import chatbot # Si chatbot est dans main.py et initialisé

        # Lire le contenu du fichier uploadé en bytes
        file_content_bytes = await file_upload.read()

        # Appeler votre logique d'ingestion avec le contenu du fichier
        # La méthode ingestion_file de votre classe Chatbot doit être adaptée
        chatbot.ingestion_file( # Assurez-vous que 'chatbot' est bien l'instance de votre classe
            base_filename=base_filename, # Utiliser le base_filename fourni par le formulaire
            file_content=file_content_bytes, # Passer le contenu du fichier
            # file_path n'est plus nécessaire ici
            departement_id=departement_id,
            filiere_id=filiere_id,
            module_id=module_id,
            activite_id=activite_id,
            profile_id=profile_id,
            user_id=user_id,
        )
        # Utiliser file_upload.filename ou base_filename pour le message
        return {"status": "success", "message": f"Fichier '{base_filename}' indexé avec succès."}
    except HTTPException as http_exc:
        # Re-lever les HTTPException pour que FastAPI les gère correctement
        raise http_exc
    except Exception as e:
        # Loggez l'erreur complète côté serveur pour le débogage
        import traceback
        traceback.print_exc()
        # Retourner une erreur générique au client
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur lors de l'ingestion: {str(e)}")

@router.get("/ingested", response_model=List[Dict])
#filter_manager.get_documents_ingested()
def get_documents():
    try:
        documents = filter_manager.get_documents_ingested()
        if not documents:
            print   ("Pas de documents ingérés.")
            # Vous pouvez choisir de retourner une liste vide ou lever une exception    
            # Par exemple, lever une HTTPException
            # 404 si vous voulez indiquer que la ressource n'existe pas

            raise HTTPException(status_code=404, detail="Pas de documents trouvés.")
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@router.get("/stats", response_model=StatsResponse) # MODIFIÉ
def get_statistics():
    try:
        stats_data = filter_manager.get_ingestion_statistics()
        if not stats_data: # Ou une vérification plus spécifique
            # Il est souvent préférable de retourner des stats vides/zéro que 404
            # Par exemple, initialiser un StatsResponse avec des valeurs par défaut
            return StatsResponse(
                total_documents=0,
                ingested_today=0,
                ingested_this_week=0,
                ingested_this_month=0,
                documents_par_departement=[],
                documents_par_filiere=[],
                documents_par_module=[],
                documents_par_activite=[]
            )
        return stats_data # FastAPI validera que stats_data correspond à StatsResponse
    except Exception as e:
        # Loggez l'erreur côté serveur pour le débogage
        print(f"Error fetching statistics: {e}") # Ou utilisez un vrai logger
        raise HTTPException(status_code=500, detail=f"Internal Server Error") # Ne pas exposer str(e) directement
    

@router.get("/chat/history", response_model=List[ChatHistoryEntry])
def get_chat_history_endpoint():
    try:
        history = filter_manager.get_chat_history()
        if not history:
            return []  # ou raise HTTPException(status_code=204, detail="No content")
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération de l’historique: {str(e)}")


#########################################################################################################

# ENDPOINTS DEPARTEMENTS
@router.get("/departements")
def get_departements():
    return manager.get_all_departements()

@router.get("/departements/{id}")
def get_departement(id: int):
    return manager.get_departement(id)

@router.post("/departements")
def add_departement(data: Departement):
    return {"id": manager.add_departement(data)}

@router.put("/departements/{id}")
def update_departement(id: int, data: Departement):
    return {"updated": manager.update_departement(id, data)}

@router.delete("/departements/{id}")
def delete_departement(id: int):
    return {"deleted": manager.delete_departement(id)}


# ENDPOINTS FILIERES
@router.get("/filieres")
def get_filieres():
    return manager.get_all_filieres()

@router.get("/filieres/{id}")
def get_filiere(id: int):
    return manager.get_filiere(id)

@router.get("/filieresByDepartement/{dep_id}")
def get_filieres_by_departement(dep_id: int):
    return manager.get_filiere_by_departement(dep_id)

@router.post("/filieres")
def add_filiere(data: Filiere):
    return {"id": manager.add_filiere(data)}

@router.put("/filieres/{id}")
def update_filiere(id: int, data: Filiere):
    return {"updated": manager.update_filiere(id, data)}

@router.delete("/filieres/{id}")
def delete_filiere(id: int):
    return {"deleted": manager.delete_filiere(id)}


# ENDPOINTS MODULES
@router.get("/modules")
def get_modules():
    return manager.get_all_modules()

@router.get("/modules/{id}")
def get_module(id: int):
    return manager.get_module(id)

@router.get("/modulesByFiliere/{filiere_id}")
def get_modules_by_filiere(filiere_id: int):
    return manager.get_module_by_filiere(filiere_id)

@router.post("/modules")
def add_module(data: Module):
    return {"id": manager.add_module(data)}

@router.put("/modules/{id}")
def update_module(id: int, data: Module):
    return {"updated": manager.update_module(id, data)}

@router.delete("/modules/{id}")
def delete_module(id: int):
    return {"deleted": manager.delete_module(id)}


# ENDPOINTS ACTIVITES
@router.get("/activites")
def get_activites():
    return manager.get_all_activites()

@router.get("/activites/{id}")
def get_activite(id: int):
    return manager.get_activite(id)

@router.post("/activites")
def add_activite(data: Activite):
    return {"id": manager.add_activite(data)}

@router.put("/activites/{id}")
def update_activite(id: int, data: Activite):
    return {"updated": manager.update_activite(id, data)}

@router.delete("/activites/{id}")
def delete_activite(id: int):
    return {"deleted": manager.delete_activite(id)}


#### ENDPOINTS RESSOURCES SUPPLÉMENTAIRES###

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/resources/", response_model=ResourceOut)
def create_resource(resource: ResourceCreate, db: Session = Depends(get_db)):
    db_resource = Resource(**resource.dict())
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@router.get("/resources/", response_model=List[ResourceOut])
def read_resources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Resource).offset(skip).limit(limit).all()

@router.get("/resources/{resource_id}", response_model=ResourceOut)
def read_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

@router.put("/resources/{resource_id}", response_model=ResourceOut)
def update_resource(resource_id: int, resource: ResourceCreate, db: Session = Depends(get_db)):
    db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    for key, value in resource.dict().items():
        setattr(db_resource, key, value)
    db.commit()
    db.refresh(db_resource)
    return db_resource

@router.delete("/resources/{resource_id}")
def delete_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    db.delete(db_resource)
    db.commit()
    return {"ok": True}

# @router.post("/ask")
# def ask(
#     req: AskRequest = Body(...),
#     db: Session = Depends(get_db)
# ):
#     # 1. Génération de la réponse via ta logique RAG
#     cleaned_llm_response = chatbot.generate_response(
#         req.user_query, req.user_id, req.profile_id, req.departement_id, req.filiere_id
#     )

#     # 2. Si demandé, récupération des ressources pertinentes
#     resources = []
#     if req.show_resources:
#         context_tags = Resource.extract_tags_from_question(req.user_query)
#         resources = Resource.get_additional_resources(db, context_tags)

#     return {
#         "answer": cleaned_llm_response,
#         "resources": [ResourceOut.from_orm(r) for r in resources]
#     }


from pydantic import BaseModel, Field
from typing import Optional,Literal, List, Union

# class ChatRequest(BaseModel):
#     message: str
#     user_id: Optional[int] = None
#     profile_id: Optional[int] = None
#     departement_id: Optional[int] = None
#     filiere_id: Optional[int] = None
#     # module_id: Optional[int] = None
#     # activite_id: Optional[int] = None

    ###Resources supplementaires des etudiants####

class ResourceCreate(BaseModel):
    type: str
    titre: str
    url: str
    tags: Optional[str] = ""

class ResourceOut(BaseModel):
    id: int
    type: str
    titre: str
    url: str
    tags: Optional[str] = ""

class Config:
    from_attributes = True


class ChatRequest(BaseModel):
    message: str
    user_id: int
    profile_id: int
    departement_id: Optional[int] = None
    filiere_id: Optional[int] = None
    show_resources: Optional[bool] = False
    
class ChatResponse(BaseModel):
    response: str
    resources: List[ResourceOut] = []    


# class ChatResponse(BaseModel):
#     response: str

class IngestRequest(BaseModel):
    base_filename : str
    file_path: str
    departement_id: Optional[int] = None
    filiere_id: Optional[int] = None
    module_id: Optional[int] = None
    activite_id: Optional[int] = None
    profile_id: Optional[int] = None
    user_id: Optional[int] = None

class DepartementStat(BaseModel):
    departement: str
    count: int

class FiliereStat(BaseModel):
    filiere: str
    count: int

class ModuleStat(BaseModel):
    module: str
    count: int

class ActiviteStat(BaseModel):
    activite: str
    count: int

class StatsResponse(BaseModel):
    total_documents: int
    ingested_today: Optional[int] = None # Si vous ajoutez les stats temporelles
    ingested_this_week: Optional[int] = None
    ingested_this_month: Optional[int] = None
    documents_par_departement: List[DepartementStat]
    documents_par_filiere: List[FiliereStat]
    documents_par_module: List[ModuleStat]
    documents_par_activite: List[ActiviteStat]



class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    message: str
    change_password_required: bool = False
    user_info: dict = None

class ChatHistoryEntry(BaseModel):
    profile: Optional[str] = None
    username: Optional[str] = None
    departement: Optional[str] = None
    filiere: Optional[str] = None
    user_query: Optional[str] = None
    chatbot_response: Optional[str] = None
    timestamp: str  # Format ISO. Tu peux formatter à l'affichage si besoin.

class ChangePasswordRequest(BaseModel):
    user_id: int
    old_password: str
    new_password: str
    
### Gestions des ressources
class Departement(BaseModel):
    id: int | None = None
    nom: str

class Filiere(BaseModel):
    id: int | None = None
    nom: str
    departement_id: int

class Module(BaseModel):
    id: int | None = None
    nom: str
    filiere_id: int

class Activite(BaseModel):
    id: int | None = None
    nom: str
    module_id: int | None = None

### Gestion CRUD  des users ####
class UserBase(BaseModel):
    username: str
    profile_id: Optional[int] = None
    filiere_id: Optional[int] = None
    annee_scolaire: Optional[str] = Field(None, alias='annee') # Utilise 'annee' en entrée, mais stocke/utilise 'annee_scolaire'

    class Config:
        orm_mode = True # Permet de mapper directement depuis des objets ORM ou des dictionnaires riches
        allow_population_by_field_name = True # Permet d'utiliser 'annee' lors de la création

class UserCreate(UserBase):
    password: str
    is_active: Optional[bool] = True
    is_default_password: Optional[bool] = True

class UserUpdate(BaseModel): # Modèle spécifique pour la mise à jour, tous les champs optionnels
    username: Optional[str] = None
    password: Optional[str] = None # Pour changer le mot de passe
    profile_id: Optional[int] = None
    filiere_id: Optional[int] = None
    annee_scolaire: Optional[str] = Field(None, alias='annee')
    is_active: Optional[bool] = None
    is_default_password: Optional[bool] = None

class Config:
    allow_population_by_field_name = True

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_default_password: bool
    # Le mot de passe n'est jamais retourné



# class AskRequest(BaseModel):
#     user_query: str
#     user_id: int
#     profile_id: int
#     departement_id: Optional[int] = None
#     filiere_id: Optional[int] = None
#     show_resources: Optional[bool] = False
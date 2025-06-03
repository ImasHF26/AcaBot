from pydantic import BaseModel
from typing import Optional,Literal, List

class ChatRequest(BaseModel):
    message: str
    departement_id: Optional[int] = None
    filiere_id: Optional[int] = None
    

class ChatResponse(BaseModel):
    response: str

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

class RegisterRequest(BaseModel):
    username: str
    password: str
    profile_id: Optional[int] = None  # 1 = Admin, 2 = Prof, 3 = Étudiant
    filiere_id: Optional[int] = None
    annee: Optional[str] = None

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
    module: Optional[str] = None
    activite: Optional[str] = None
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
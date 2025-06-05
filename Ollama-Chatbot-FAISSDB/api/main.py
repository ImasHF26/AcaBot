from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .endpoints import router


app = FastAPI(title="EduLLM API", version="1.0.0")

# Création des tables au démarrage (à faire seulement en dev)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)  
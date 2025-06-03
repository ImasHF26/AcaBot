from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .endpoints import router

app = FastAPI(title="Academic RAG Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # à restreindre en prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

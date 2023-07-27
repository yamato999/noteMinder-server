import os
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.notes.router import router as notes_router
from app.auth.router import router as auth_router
from app.config import client, env, fastapi_config

load_dotenv()
app = FastAPI(**fastapi_config)


@app.on_event("shutdown")
def shutdown_db_client():
    client.close()


CORS_METHODS = "GET,POST,PUT"
CORS_HEADERS = "Content-Type,Authorization"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=CORS_METHODS.split(","),
    allow_headers=CORS_HEADERS.split(","),
    allow_credentials=True,
)


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(notes_router, prefix="/notes", tags=["Notes"])

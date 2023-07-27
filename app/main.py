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


app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS").split(","),
    allow_methods=os.getenv("CORS_METHODS").split(","),
    allow_headers=os.getenv("CORS_HEADERS").split(","),
    allow_credentials=True,
)


app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(notes_router, prefix="/notes", tags=["Notes"])

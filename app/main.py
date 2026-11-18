
from fastapi import FastAPI
from app.routes.scans import router as scans_router

app = FastAPI(title="Secure Code Review Tool")


@app.get("/")
def home():
    return {
        "message": "Welcome to the Secure Code Review Tool!"
    }

app.include_router(scans_router)
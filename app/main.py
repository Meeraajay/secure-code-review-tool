
from fastapi import FastAPI

app = FastAPI(title="Secure Code Review Tool")


@app.get("/")
def home():
    return {
        "message": "Welcome to the Secure Code Review Tool!"
    }

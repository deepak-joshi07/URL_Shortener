from fastapi import FastAPI
from app.routes import api_router , redirect_router

app = FastAPI(title="Short Link API")

app.include_router(api_router)
app.include_router(redirect_router)

@app.get("/")
def health():
    return {"status": "ok"}
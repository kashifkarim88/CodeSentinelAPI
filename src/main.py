from fastapi import FastAPI
from src.api.analyze import router

app = FastAPI(title="Code Sentinel API")
app.include_router(router)
@app.get("/health")
def health_check():
    return {"status": "online", "version": "1.0.0"}
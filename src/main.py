from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.analyze import router

app = FastAPI(title="Code Sentinel API")

# 1. Configure CORS
# During development, ["*"] allows all origins. 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

# 2. Include Routers
app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "online", "version": "1.0.0"}
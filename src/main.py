from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.analyze import router

app = FastAPI(title="Code Sentinel API")

# 1. Configure CORS
# During development, ["*"] allows all origins. 
# Once you deploy your Next.js app to Vercel, you can replace "*" with your Vercel URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],  # Allows POST, GET, OPTIONS, etc.
    allow_headers=["*"],  # Allows all headers (Content-Type, etc.)
)

# 2. Include Routers
app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "online", "version": "1.0.0"}
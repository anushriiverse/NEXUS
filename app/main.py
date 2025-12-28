from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import research
import uvicorn
import os
from app.routers import ai


app = FastAPI(
    title="TechInsight Research Backend",
    description="Backend API for fetching and storing research papers from arXiv (using SQLite).",
    version="1.0.0"
)
app = FastAPI()

app.include_router(ai.router, prefix="/ai")

@app.get("/")
def root():
    return {"status": "TechInsight backend running"}

# Configure CORS
# Allow all origins for the hackathon MVP. 
# In production, restrict this to the frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(research.router)

@app.get("/")
async def root():
    return {"message": "TechInsight Research API is running. Go to /docs for Swagger UI."}

if __name__ == "__main__":
    # Use PORT env var for Cloud Run, default to 8000 locally
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)


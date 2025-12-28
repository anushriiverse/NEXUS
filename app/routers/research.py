from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.models import ResearchPaper
from app.services.arxiv_service import ArxivService
from app.services.sqlite_service import SqliteService

router = APIRouter(
    prefix="/research",
    tags=["research"]
)

# Initialize services
# In a larger app, use dependency injection
arxiv_service = ArxivService()
db_service = SqliteService()

@router.post("/sync")
def sync_research(query: str = "cs.AI"):
    service = ArxivService()
    sqlite = SqliteService()
    papers = service.fetch_papers(query=query, max_results=10)
    sqlite.save_papers(papers)
    return {
        "status": "success",
        "fetched": len(papers)
    }


@router.get("/latest", response_model=List[ResearchPaper])
async def get_latest_research():
    """
    Get the latest research papers (defaulting to CS/AI categories).
    Fetches from arXiv, caches in SQLite, and returns the results.
    """
    try:
        # 1. Fetch from arXiv
        papers = arxiv_service.fetch_latest_cs_papers()
        
        # 2. Store in SQLite
        if papers:
            db_service.save_papers(papers)
            
        return papers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/topic/{topic}", response_model=List[ResearchPaper])
async def get_research_by_topic(topic: str):
    """
    Get research papers for a specific topic.
    Fetches from arXiv, caches in Firestore, and returns the results.
    """
    try:
        # 1. Fetch from arXiv
        # Construct a query for the topic
        query = f"all:{topic}"
        papers = arxiv_service.fetch_papers(query=query)
        
        # 2. Store in SQLite
        if papers:
            db_service.save_papers(papers)
            
        return papers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

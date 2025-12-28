from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ResearchPaper(BaseModel):
    """
    Data model representing a research paper from arXiv.
    Used for both API responses and Firestore storage.
    """
    id: str  # arXiv ID (e.g., "2101.12345")
    title: str
    authors: List[str]
    abstract: str
    categories: List[str]
    published_date: datetime
    pdf_link: str
    
    class Config:
        # Allow population by field name for compatibility
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "id": "2312.12345",
                "title": "Advances in Computer Vision",
                "authors": ["Jane Doe", "John Smith"],
                "abstract": "This paper explores...",
                "categories": ["cs.CV", "cs.AI"],
                "published_date": "2023-12-28T10:00:00",
                "pdf_link": "http://arxiv.org/pdf/2312.12345v1"
            }
        }

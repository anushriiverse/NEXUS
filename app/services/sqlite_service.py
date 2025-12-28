import sqlite3
import json
from typing import List
from app.models import ResearchPaper
from datetime import datetime

class SqliteService:
    """
    Service to interact with SQLite database.
    Handles storage and retrieval of research paper metadata.
    """
    
    def __init__(self, db_path="techinsight.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database table if it doesn't exist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS papers (
                        id TEXT PRIMARY KEY,
                        title TEXT,
                        authors TEXT,
                        abstract TEXT,
                        categories TEXT,
                        published_date TEXT,
                        pdf_link TEXT
                    )
                ''')
                conn.commit()
        except Exception as e:
            print(f"Error initializing SQLite DB: {e}")

    def save_papers(self, papers: List[ResearchPaper]):
        """
        Batch writes papers to SQLite.
        Uses INSERT OR REPLACE to handle duplicates.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                for paper in papers:
                    # Serialize lists to JSON strings for storage
                    authors_json = json.dumps(paper.authors)
                    categories_json = json.dumps(paper.categories)
                    # ISO format for date
                    date_str = paper.published_date.isoformat()
                    
                    cursor.execute('''
                        INSERT OR REPLACE INTO papers 
                        (id, title, authors, abstract, categories, published_date, pdf_link)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (paper.id, paper.title, authors_json, paper.abstract, 
                          categories_json, date_str, paper.pdf_link))
                conn.commit()
                print(f"Successfully saved {len(papers)} papers to SQLite.")
        except Exception as e:
            print(f"Error saving to SQLite: {e}")

    def get_papers_by_topic(self, topic: str, limit: int = 20) -> List[ResearchPaper]:
        """
        Retrieves papers from SQLite.
        Simple implementation that returns latest papers, 
        optionally filtering if we implemented full search.
        """
        papers = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                
                # Basic query - in a real app we'd add WHERE clauses for topic filtering
                # if we were searching the DB.
                cursor.execute('SELECT * FROM papers ORDER BY published_date DESC LIMIT ?', (limit,))
                rows = cursor.fetchall()
                
                for row in rows:
                    papers.append(ResearchPaper(
                        id=row['id'],
                        title=row['title'],
                        authors=json.loads(row['authors']),
                        abstract=row['abstract'],
                        categories=json.loads(row['categories']),
                        published_date=datetime.fromisoformat(row['published_date']),
                        pdf_link=row['pdf_link']
                    ))
        except Exception as e:
            print(f"Error reading from SQLite: {e}")
            
        return papers

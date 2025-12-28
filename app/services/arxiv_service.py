import arxiv
from typing import List
from app.models import ResearchPaper

class ArxivService:
    """
    Service to interact with the arXiv API.
    Encapsulates the logic for fetching and parsing paper metadata.
    """
    
    def __init__(self):
        # Initialize the client with default settings
        self.client = arxiv.Client(
            page_size=10,
            delay_seconds=3,
            num_retries=3
        )

    def fetch_papers(self, query: str, max_results: int = 20) -> List[ResearchPaper]:
        """
        Fetches papers from arXiv based on a search query.
        
        Args:
            query: The search query (e.g., "cat:cs.AI" or "machine learning")
            max_results: Maximum number of papers to return
            
        Returns:
            List[ResearchPaper]: A list of parsed research paper objects
        """
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )

        papers = []
        try:
            results = self.client.results(search)
            for result in results:
                # Map arxiv.Result to our ResearchPaper model
                paper = ResearchPaper(
                    id=result.entry_id.split('/')[-1], # Extract ID from URL
                    title=result.title,
                    authors=[author.name for author in result.authors],
                    abstract=result.summary,
                    categories=result.categories,
                    published_date=result.published,
                    pdf_link=result.pdf_url
                )
                papers.append(paper)
        except Exception as e:
            print(f"Error fetching from arXiv: {e}")
            # In a real app, we might want to log this properly or raise a custom exception
            return []

        return papers

    def fetch_latest_cs_papers(self, max_results: int = 20) -> List[ResearchPaper]:
        """
        Convenience method to fetch the latest Computer Science papers.
        """
        return self.fetch_papers(query="cat:cs.AI OR cat:cs.LG OR cat:cs.SE", max_results=max_results)

"""Pydantic schemas for structured data used in the research assistant."""

from pydantic import BaseModel
from typing import Optional


class SearchResult(BaseModel):
    """Represents a single web search result."""

    query: str
    content: str
    source_url: Optional[str] = None


class ResearchSummary(BaseModel):
    """Represents a summarized research output."""

    topic: str
    summary: str
    key_points: list[str] = []

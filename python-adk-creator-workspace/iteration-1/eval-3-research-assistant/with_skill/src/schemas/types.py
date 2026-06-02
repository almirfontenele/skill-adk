"""Pydantic models for structured data in the Research Assistant."""

from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    """Model for a web search query."""

    query: str = Field(..., description="The search query string")
    max_results: int = Field(5, ge=1, le=10, description="Maximum number of results")


class SummarySummary(BaseModel):
    """Model for a content summary."""

    content: str = Field(..., description="The content to summarize")
    max_length: int = Field(200, ge=50, le=1000, description="Maximum summary length")


class SearchResult(BaseModel):
    """Model for a single search result."""

    title: str = Field(..., description="The result title")
    url: str = Field(..., description="The result URL")
    snippet: str = Field(..., description="A brief snippet of the result")

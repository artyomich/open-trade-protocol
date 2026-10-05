"""Search service for PEP Index."""

from __future__ import annotations

from typing import Optional, List
from app.services.index.aggregator import ListingAggregator


class SearchService:
    """Search service for PEP Index."""
    
    def __init__(self, aggregator: ListingAggregator):
        self.aggregator = aggregator
    
    async def search(
        self,
        query: str,
        category: Optional[str] = None,
        condition: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        buyer_lat: Optional[float] = None,
        buyer_lon: Optional[float] = None,
        sort: str = "relevance_score",
        limit: int = 20,
        cursor: Optional[str] = None,
    ) -> dict:
        """Search across all federated nodes."""
        return await self.aggregator.search_listings(
            query=query,
            category=category,
            condition=condition,
            price_min=price_min,
            price_max=price_max,
            limit=limit,
            cursor=cursor,
        )
    
    async def semantic_search(
        self,
        vector: List[float],
        category: Optional[str] = None,
        buyer_lat: Optional[float] = None,
        buyer_lon: Optional[float] = None,
        limit: int = 20,
    ) -> dict:
        """Semantic search using vector embeddings."""
        # In production, would query Qdrant vector store
        return await self.aggregator.search_listings(
            query="semantic_search",
            category=category,
            limit=limit,
        )
    
    async def get_category_schema(self, category_id: str) -> Optional[dict]:
        """Get JSON Schema for a product category."""
        # In production, would load from schema registry
        if category_id == "winter_sports/snowboard":
            return {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$id": "https://opentradeprotocol.com/schemas/v1/category/winter_sports/snowboard.json",
                "title": "Snowboard",
                "type": "object",
                "required": ["category", "brand", "model", "condition", "specifications"],
            }
        return None

"""Listing aggregator for PEP Index."""

from __future__ import annotations

import asyncio
import json
import hashlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from app.core.config import settings
from app.core.logging import get_logger
from app.services.index.registry import NodeRegistry


logger = get_logger("index.aggregator")


class ListingAggregator:
    """Aggregates listings from all federation nodes."""
    
    def __init__(self, registry: Optional[NodeRegistry] = None):
        self.registry = registry
        self._listings: Dict[str, dict] = {}  # listing_id -> listing
        self._node_listings: Dict[str, set] = {}  # node_id -> set of listing_ids
        self._running = False
        self._sync_task = None
    
    async def initialize(self) -> None:
        """Initialize the aggregator."""
        logger.info("Initializing listing aggregator...")
        self._running = True
        self._sync_task = asyncio.create_task(self._sync_loop())
        logger.info("Listing aggregator initialized")
    
    async def stop(self) -> None:
        """Stop the aggregator."""
        self._running = False
        if self._sync_task:
            self._sync_task.cancel()
            try:
                await self._sync_task
            except asyncio.CancelledError:
                pass
    
    async def announce_listings(
        self,
        node_id: str,
        listings: List[dict],
        signature: str,
    ) -> dict:
        """Process listing announcements from a node."""
        logger.info("Processing listing announcement", node_id=node_id, count=len(listings))
        
        # Verify node exists and is active
        node = await self.registry.get_node(node_id) if self.registry else None
        if not node or node.get("status") != "active":
            return {"status": "rejected", "reason": "Node not active"}
        
        # Verify signature (in production, would verify Ed25519 signature)
        # For now, trust the node
        added = 0
        updated = 0
        
        for listing in listings:
            listing_id = listing.get("listingId", listing.get("listing_id", ""))
            if not listing_id:
                continue
            
            if listing_id in self._listings:
                # Update existing listing
                self._listings[listing_id].update(listing)
                updated += 1
            else:
                # Add new listing
                self._listings[listing_id] = listing
                added += 1
            
            # Track node-listing relationship
            if node_id not in self._node_listings:
                self._node_listings[node_id] = set()
            self._node_listings[node_id].add(listing_id)
        
        # Update node listings count
        if self.registry and node_id in self.registry._nodes:
            self.registry._nodes[node_id].listings_count = len(
                self._node_listings.get(node_id, set())
            )
        
        logger.info("Listing announcement processed", added=added, updated=updated)
        return {
            "status": "accepted",
            "added": added,
            "updated": updated,
            "totalListings": len(self._listings),
        }
    
    async def get_listing(self, listing_id: str) -> Optional[dict]:
        """Get a listing by ID."""
        return self._listings.get(listing_id)
    
    async def search_listings(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        condition: Optional[str] = None,
        price_min: Optional[float] = None,
        price_max: Optional[float] = None,
        limit: int = 20,
        cursor: Optional[str] = None,
    ) -> dict:
        """Search aggregated listings."""
        results = list(self._listings.values())
        
        # Apply filters
        if category:
            results = [
                r for r in results
                if r.get("product", {}).get("category", "").startswith(category)
            ]
        
        if condition:
            results = [
                r for r in results
                if r.get("product", {}).get("condition", {}).get("overallGrade") == condition
            ]
        
        if price_min:
            results = [
                r for r in results
                if r.get("pricing", {}).get("askPrice", {}).get("amount", 0) >= price_min
            ]
        
        if price_max:
            results = [
                r for r in results
                if r.get("pricing", {}).get("askPrice", {}).get("amount", float("inf")) <= price_max
            ]
        
        # Sort by relevance (simplified)
        results.sort(key=lambda x: x.get("aiConfidence", 0), reverse=True)
        
        # Pagination
        start = 0
        if cursor:
            try:
                start = int(cursor.split(":")[1])
            except (ValueError, IndexError):
                start = 0
        
        end = start + limit
        paginated = results[start:end]
        
        next_cursor = str(end) if end < len(results) else None
        
        return {
            "results": paginated,
            "total_estimated": len(results),
            "next_cursor": next_cursor,
            "search_metadata": {
                "query_understood_as": query or "",
                "semantic_fallback_used": False,
                "execution_time_ms": 12,
            },
        }
    
    async def get_node_listings(self, node_id: str) -> List[dict]:
        """Get all listings from a specific node."""
        listing_ids = self._node_listings.get(node_id, set())
        return [self._listings[lid] for lid in listing_ids if lid in self._listings]
    
    async def get_listings_by_category(self, category: str) -> List[dict]:
        """Get all listings for a specific category."""
        return [
            r for r in self._listings.values()
            if r.get("product", {}).get("category", "").startswith(category)
        ]
    
    async def bulk_listings(
        self,
        updated_since: Optional[str] = None,
        categories: Optional[List[str]] = None,
        cursor: Optional[str] = None,
        limit: int = 100,
    ) -> dict:
        """Bulk fetch listings for indexing."""
        results = list(self._listings.values())
        
        if categories:
            results = [
                r for r in results
                if any(
                    r.get("product", {}).get("category", "").startswith(cat)
                    for cat in categories
                )
            ]
        
        # Pagination
        start = 0
        if cursor:
            try:
                start = int(cursor.split(":")[1])
            except (ValueError, IndexError):
                start = 0
        
        end = start + limit
        paginated = results[start:end]
        
        next_cursor = str(end) if end < len(results) else None
        
        return {
            "listings": paginated,
            "next_cursor": next_cursor,
            "total_available": len(results),
        }
    
    async def _sync_loop(self) -> None:
        """Periodically sync with all nodes."""
        while self._running:
            try:
                if self.registry:
                    nodes = await self.registry.get_active_nodes()
                    for node in nodes:
                        # In production, would fetch updates from node
                        logger.debug("Syncing with node", node_id=node.node_id)
            except Exception as e:
                logger.error("Sync failed", error=str(e))
            
            await asyncio.sleep(settings.federation_sync_interval)

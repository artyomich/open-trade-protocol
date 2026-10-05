"""API v1 router for PEP Index."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import uuid

from app.services.index.registry import NodeRegistry
from app.services.index.aggregator import ListingAggregator
from app.services.federation.sync import FederationSync
from app.services.trust.service import TrustService
from app.services.search.service import SearchService


router = APIRouter()

# Service instances (would be injected via DI in production)
registry = NodeRegistry()
aggregator = ListingAggregator(registry)
federation = FederationSync()
trust = TrustService()
search = SearchService(aggregator)


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "pep-index",
        "version": "0.1.0-draft",
        "nodes": len(await registry.get_active_nodes()),
        "listings": len(aggregator._listings),
    }


# === Node Registration ===

@router.post("/federation/register")
async def register_node(
    node_id: str = Query(..., description="Node identifier"),
    node_public_key: str = Query(..., description="Ed25519 public key"),
    node_url: str = Query(..., description="Node API URL"),
    capabilities: str = Query("search,escrow", description="Comma-separated capabilities"),
    supported_categories: str = Query("", description="Comma-separated categories"),
    contact_email: str = Query("", description="Contact email"),
    contact_website: str = Query("", description="Contact website"),
):
    """Register a new federation node."""
    caps = [c.strip() for c in capabilities.split(",") if c.strip()]
    cats = [c.strip() for c in supported_categories.split(",") if c.strip()]
    contact = {"email": contact_email, "website": contact_website}
    
    result = await registry.register_node(
        node_id=node_id,
        node_public_key=node_public_key,
        node_url=node_url,
        capabilities=caps,
        supported_categories=cats,
        contact=contact,
    )
    return result


@router.get("/federation/nodes")
async def list_nodes(status: Optional[str] = Query(None, description="Filter by status")):
    """List all registered nodes."""
    nodes = await registry.list_nodes(status=status)
    return {"nodes": nodes}


@router.get("/federation/nodes/{node_id}")
async def get_node(node_id: str):
    """Get a node by ID."""
    node = await registry.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


# === Federation Sync ===

@router.post("/federation/announce")
async def announce_listings(
    node_id: str = Query(..., description="Node identifier"),
    signature: str = Query(..., description="Listing signature"),
    listings: str = Query("", description="Comma-separated listing IDs"),
):
    """Announce listings to the index."""
    listing_ids = [lid.strip() for lid in listings.split(",") if lid.strip()]
    
    # In production, would fetch full listing data
    result = await aggregator.announce_listings(
        node_id=node_id,
        listings=[{"listingId": lid} for lid in listing_ids],
        signature=signature,
    )
    return result


@router.post("/federation/heartbeat")
async def heartbeat(
    node_id: str = Query(..., description="Node identifier"),
):
    """Send heartbeat from a node."""
    result = await federation.heartbeat(node_id)
    return result


@router.get("/federation/sync/full")
async def sync_full(node_id: str = Query(..., description="Node identifier")):
    """Get full sync data from a node."""
    listings = await aggregator.get_node_listings(node_id)
    return {"listings": listings}


@router.get("/federation/sync/incremental")
async def sync_incremental(
    node_id: str = Query(..., description="Node identifier"),
    updated_since: str = Query(..., description="Updated since timestamp"),
):
    """Get incremental sync data from a node."""
    listings = await aggregator.get_node_listings(node_id)
    return {"listings": listings}


@router.post("/federation/recover")
async def recover_node(
    node_id: str = Query(..., description="Node identifier"),
    new_public_key: str = Query(..., description="New public key"),
):
    """Recover a suspended node."""
    await registry.unsuspend_node(node_id)
    return {"nodeId": node_id, "status": "active"}


# === Search ===

@router.post("/search")
async def search_listings(
    query: str = Query(..., description="Search query"),
    category: Optional[str] = Query(None, description="Category filter"),
    condition: Optional[str] = Query(None, description="Condition filter"),
    price_min: Optional[float] = Query(None, description="Minimum price"),
    price_max: Optional[float] = Query(None, description="Maximum price"),
    sort: str = Query("relevance_score", description="Sort order"),
    limit: int = Query(20, ge=1, le=100, description="Max results"),
    cursor: Optional[str] = Query(None, description="Pagination cursor"),
):
    """Search across all federated nodes."""
    results = await search.search(
        query=query,
        category=category,
        condition=condition,
        price_min=price_min,
        price_max=price_max,
        sort=sort,
        limit=limit,
        cursor=cursor,
    )
    return results


@router.post("/search/semantic")
async def semantic_search(
    vector: str = Query(..., description="Comma-separated embedding vector"),
    category: Optional[str] = Query(None, description="Category filter"),
    limit: int = Query(20, ge=1, le=100, description="Max results"),
):
    """Semantic search using vector embeddings."""
    vector_list = [float(x) for x in vector.split(",") if x.strip()]
    results = await search.semantic_search(
        vector=vector_list,
        category=category,
        limit=limit,
    )
    return results


# === Listings ===

@router.get("/listings/{listing_id}")
async def get_listing(listing_id: str):
    """Get a listing by ID."""
    listing = await aggregator.get_listing(listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing


@router.get("/listings/bulk")
async def bulk_listings(
    updated_since: Optional[str] = Query(None, description="Updated since"),
    categories: Optional[str] = Query(None, description="Categories filter"),
    cursor: Optional[str] = Query(None, description="Pagination cursor"),
    limit: int = Query(100, ge=1, le=1000, description="Max results"),
):
    """Bulk fetch listings for indexing."""
    cat_list = [c.strip() for c in categories.split(",")] if categories else None
    result = await aggregator.bulk_listings(
        updated_since=updated_since,
        categories=cat_list,
        cursor=cursor,
        limit=limit,
    )
    return result


# === Trust ===

@router.get("/trust/{did}")
async def get_trust_score(did: str):
    """Get trust score for a DID."""
    score = await trust.get_trust_score(did)
    if not score:
        cross_node = await trust.compute_cross_node_trust(did)
        return {"trustScore": cross_node}
    return {"trustScore": score}


# === Categories ===

@router.get("/categories/{category_id}/schema")
async def get_category_schema(category_id: str):
    """Get JSON Schema for a product category."""
    schema = await search.get_category_schema(category_id)
    if not schema:
        raise HTTPException(status_code=404, detail="Category schema not found")
    return schema


# === Logistics ===

@router.post("/logistics/calculate")
async def calculate_logistics(
    origin_lat: float = Query(..., description="Origin latitude"),
    origin_lon: float = Query(..., description="Origin longitude"),
    destination_lat: float = Query(..., description="Destination latitude"),
    destination_lon: float = Query(..., description="Destination longitude"),
    length_cm: float = Query(..., description="Package length"),
    width_cm: float = Query(..., description="Package width"),
    height_cm: float = Query(..., description="Package height"),
    weight_kg: float = Query(..., description="Package weight"),
    declared_value: float = Query(..., description="Declared value"),
    insurance: bool = Query(True, description="Include insurance"),
):
    """Calculate shipping options."""
    # In production, would integrate with logistics providers
    return {
        "options": [
            {
                "carrier": "cdek",
                "service": "express",
                "cost": 890,
                "insuranceCost": 140,
                "daysMin": 2,
                "daysMax": 4,
                "tracking": True,
            },
            {
                "carrier": "russian_post",
                "service": "parcel",
                "cost": 450,
                "insuranceCost": 90,
                "daysMin": 5,
                "daysMax": 10,
                "tracking": True,
            },
        ],
        "totalLandedCost": {
            "product": declared_value,
            "shipping": 890,
            "insurance": 140,
            "platformFee": declared_value * 0.015,
            "total": declared_value + 890 + 140 + declared_value * 0.015,
        },
    }

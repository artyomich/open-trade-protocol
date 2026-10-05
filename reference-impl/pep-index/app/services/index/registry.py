"""Node registry for PEP Index."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

from app.core.config import settings
from app.core.logging import get_logger


logger = get_logger("index.registry")


class Node:
    """Registered federation node."""
    
    def __init__(
        self,
        node_id: str,
        node_public_key: str,
        node_url: str,
        capabilities: List[str],
        supported_categories: List[str],
        contact: Dict[str, str],
    ):
        self.node_id = node_id
        self.node_public_key = node_public_key
        self.node_url = node_url
        self.capabilities = capabilities
        self.supported_categories = supported_categories
        self.contact = contact
        self.status = "active"
        self.registered_at = datetime.utcnow()
        self.last_heartbeat = datetime.utcnow()
        self.listings_count = 0
        self.health_score = 1.0
    
    def to_dict(self) -> dict:
        return {
            "nodeId": self.node_id,
            "nodePublicKey": self.node_public_key,
            "nodeUrl": self.node_url,
            "capabilities": self.capabilities,
            "supportedCategories": self.supported_categories,
            "contact": self.contact,
            "status": self.status,
            "registeredAt": self.registered_at.isoformat(),
            "lastHeartbeat": self.last_heartbeat.isoformat(),
            "listingsCount": self.listings_count,
            "healthScore": self.health_score,
        }
    
    def heartbeat(self) -> None:
        """Update heartbeat timestamp."""
        self.last_heartbeat = datetime.utcnow()
        self.health_score = min(1.0, self.health_score + 0.1)
    
    def check_health(self) -> bool:
        """Check if node is healthy."""
        return (datetime.utcnow() - self.last_heartbeat).seconds < 900  # 15 minutes


class NodeRegistry:
    """Registry of federation nodes."""
    
    def __init__(self):
        self._nodes: Dict[str, Node] = {}
        self._max_nodes = settings.federation_max_nodes
        self._running = False
        self._health_check_task = None
    
    async def initialize(self) -> None:
        """Initialize the node registry."""
        logger.info("Initializing node registry...")
        self._running = True
        self._health_check_task = asyncio.create_task(self._health_check_loop())
        logger.info(f"Node registry initialized (max nodes: {self._max_nodes})")
    
    async def stop(self) -> None:
        """Stop the node registry."""
        self._running = False
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass
    
    async def register_node(
        self,
        node_id: str,
        node_public_key: str,
        node_url: str,
        capabilities: List[str],
        supported_categories: List[str],
        contact: Dict[str, str],
    ) -> dict:
        """Register a new federation node."""
        logger.info("Registering node", node_id=node_id)
        
        if node_id in self._nodes:
            # Update existing node
            node = self._nodes[node_id]
            node.node_public_key = node_public_key
            node.node_url = node_url
            node.capabilities = capabilities
            node.supported_categories = supported_categories
            node.contact = contact
            node.status = "active"
            node.registered_at = datetime.utcnow()
            node.health_score = 1.0
        else:
            if len(self._nodes) >= self._max_nodes:
                raise ValueError(f"Maximum number of nodes reached ({self._max_nodes})")
            
            node = Node(
                node_id=node_id,
                node_public_key=node_public_key,
                node_url=node_url,
                capabilities=capabilities,
                supported_categories=supported_categories,
                contact=contact,
            )
            self._nodes[node_id] = node
        
        logger.info("Node registered successfully", node_id=node_id)
        return node.to_dict()
    
    async def get_node(self, node_id: str) -> Optional[dict]:
        """Get a node by ID."""
        node = self._nodes.get(node_id)
        return node.to_dict() if node else None
    
    async def list_nodes(self, status: Optional[str] = None) -> List[dict]:
        """List all registered nodes."""
        nodes = list(self._nodes.values())
        
        if status:
            nodes = [n for n in nodes if n.status == status]
        
        return [n.to_dict() for n in nodes]
    
    async def suspend_node(self, node_id: str) -> bool:
        """Suspend a node."""
        node = self._nodes.get(node_id)
        if node:
            node.status = "suspended"
            logger.warning("Node suspended", node_id=node_id)
            return True
        return False
    
    async def unsuspend_node(self, node_id: str) -> bool:
        """Unsuspend a node."""
        node = self._nodes.get(node_id)
        if node and node.status == "suspended":
            node.status = "active"
            node.health_score = 1.0
            logger.info("Node unsuspended", node_id=node_id)
            return True
        return False
    
    async def remove_node(self, node_id: str) -> bool:
        """Remove a node from the registry."""
        if node_id in self._nodes:
            del self._nodes[node_id]
            logger.info("Node removed", node_id=node_id)
            return True
        return False
    
    async def get_active_nodes(self) -> List[Node]:
        """Get all active nodes."""
        return [n for n in self._nodes.values() if n.status == "active"]
    
    async def get_nodes_by_category(self, category: str) -> List[Node]:
        """Get nodes that support a specific category."""
        return [
            n for n in self._nodes.values()
            if n.status == "active" and category in n.supported_categories
        ]
    
    async def _health_check_loop(self) -> None:
        """Periodically check node health."""
        while self._running:
            try:
                for node_id, node in list(self._nodes.items()):
                    if not node.check_health():
                        logger.warning("Node unhealthy", node_id=node_id)
                        node.health_score = max(0, node.health_score - 0.1)
                        
                        if node.health_score <= 0:
                            await self.suspend_node(node_id)
            except Exception as e:
                logger.error("Health check failed", error=str(e))
            
            await asyncio.sleep(60)  # Check every minute

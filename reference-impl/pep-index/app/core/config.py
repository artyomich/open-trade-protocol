"""PEP Index configuration."""

from __future__ import annotations

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """PEP Index settings."""
    
    # Index configuration
    index_url: str = "https://api.opentrades.io/v1"
    index_name: str = "OpenTrade PEP Index"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8001
    debug: bool = False
    
    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/pep_index"
    
    # Search
    meilisearch_url: str = "http://localhost:7700"
    meilisearch_master_key: str = ""
    qdrant_url: str = "http://localhost:6333"
    
    # Federation
    federation_heartbeat_interval: int = 300
    federation_sync_interval: int = 60
    federation_max_nodes: int = 1000
    
    # Rate limiting
    rate_limit_default: int = 1000  # requests per minute
    rate_limit_agent: int = 5000
    rate_limit_node: int = 10000
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_prefix = "PEP_INDEX_"
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

"""CLI for PEP Index."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.logging import setup_logging, get_logger


logger = get_logger("cli")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="PEP Index CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Register command
    register_parser = subparsers.add_parser("register", help="Register node with PEP Index")
    
    # Migrate command
    migrate_parser = subparsers.add_parser("migrate", help="Run database migrations")
    migrate_parser.add_argument("action", choices=["up", "down"], help="Migration action")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Start the PEP Index")
    
    args = parser.parse_args()
    
    if args.command == "register":
        register_node()
    elif args.command == "migrate":
        run_migrate(args.action)
    elif args.command == "run":
        run_node()
    else:
        parser.print_help()


async def register_node():
    """Register this node with the PEP Index."""
    setup_logging()
    logger.info("Registering node with PEP Index...")
    print("Registration completed.")


def run_migrate(action: str):
    """Run database migrations."""
    print(f"Running migrations ({action})...")
    print("Not implemented yet. Use alembic for production migrations.")


def run_node():
    """Start the PEP Index."""
    from app.main import main as start_main
    start_main()


if __name__ == "__main__":
    import asyncio
    main()

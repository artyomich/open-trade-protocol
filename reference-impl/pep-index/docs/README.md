"""PEP Index documentation."""

# PEP Index — Federated Index for OpenTrade Protocol

The PEP Index aggregates listings from all federated nodes and provides
a unified search interface for AI agents.

## Architecture

- **Node Registry**: Tracks all registered nodes and their capabilities
- **Listing Aggregator**: Aggregates listings from all nodes with deduplication
- **Search Service**: Full-text + semantic search via Meilisearch + Qdrant
- **Trust Service**: Cross-node trust scores and reputation
- **Federation Sync**: Heartbeat monitoring and incremental sync

## Quick Start

```bash
# Clone and setup
git clone https://github.com/open-trade-protocol/pep-index
cd pep-index
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure
cp config/settings.example.yaml config/settings.yaml
# Edit config/settings.yaml

# Run with docker-compose
docker-compose up -d
```

## API Endpoints

### Node Registration
```bash
curl -X POST https://api.opentradeprotocol.com/v1/federation/register \
  -d "nodeId=snow.opentradeprotocol.com" \
  -d "nodePublicKey=<key>" \
  -d "nodeUrl=https://snow.opentradeprotocol.com/v1" \
  -d "capabilities=search,escrow" \
  -d "supportedCategories=winter_sports/snowboard"
```

### Announce Listings
```bash
curl -X POST https://api.opentradeprotocol.com/v1/federation/announce \
  -d "nodeId=snow.opentradeprotocol.com" \
  -d "signature=<sig>" \
  -d "listings=lst_123,lst_456"
```

### Heartbeat
```bash
curl -X POST https://api.opentradeprotocol.com/v1/federation/heartbeat \
  -d "nodeId=snow.opentradeprotocol.com"
```

### Search
```bash
curl -X POST https://api.opentradeprotocol.com/v1/search \
  -d "query=Jones Flagship 158" \
  -d "category=winter_sports/snowboard" \
  -d "condition=good" \
  -d "limit=20"
```

## Testing

```bash
python -m pytest tests/
```

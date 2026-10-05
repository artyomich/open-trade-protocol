# OpenTrade Protocol

**Open protocol for structured peer-to-peer commerce, optimized for AI agent consumption.**

Any marketplace can publish listings. AI agents discover and transact across all nodes using a single API.

> **Vision:** Become the HTTP for P2P commerce. When AI agents make purchasing decisions, they need one protocol, not 50 different APIs.

---

## Quick Links

- [Protocol Plan](PLAN.md) — architecture decisions, GTM strategy, tech stack
- [OpenAPI Spec](spec/openapi/openapi.yaml) — full API contract for AI agents
- [JSON-LD Context](spec/schemas/json-ld/context.jsonld) — semantic schema definitions
- [Federation Protocol](spec/protocols/federation/PROTOCOL.md) — how nodes publish listings
- [Escrow Protocol](spec/protocols/escrow/PROTOCOL.md) — secure transaction lifecycle
- [Negotiation Protocol](spec/protocols/negotiation/PROTOCOL.md) — AI agent price negotiation
- [Examples](spec/examples/) — real listing, escrow, and offer data

## Why OpenTrade

| Problem | OpenTrade Solution |
|---|---|
| AI agents need 50 different marketplace APIs | One protocol, one API |
| Unstructured listings are useless to AI | JSON-LD + JSON Schema validation |
| Price comparison requires shipping cost | `total_landed_cost` on every listing |
| Trust is subjective star ratings | Computed trust graph with AI-verified metrics |
| No programmable negotiation | DID-signed offers with AI reasoning |
| Centralized platforms control data | Federated nodes, no gatekeeper |

## Protocol Components

### 1. Data Schema
- **JSON-LD** for semantic interoperability (Schema.org compatible)
- **JSON Schema v2020-12** per category for strict validation
- All critical fields typed: enums, numbers, references — no free text

### 2. Search & Discovery
- `POST /v1/search` — structured + semantic search
- `POST /v1/search/semantic` — vector embedding search
- Results sorted by `relevance_score` and `total_landed_cost`
- Cursor-based pagination, ETag support

### 3. Negotiation
- `POST /v1/listings/{id}/offers` — machine-readable offers
- AI agents accept, reject, or counter-offer automatically
- Offers signed with buyer DID, include AI reasoning

### 4. Escrow
- State machine: CREATED -> FUNDED -> SHIPPED -> DELIVERED -> INSPECTING -> CONFIRMED -> SETTLED
- 48-hour inspection window
- PIN confirmation or AI photo verification
- Dispute resolution with arbitration

### 5. Trust Graph
- DID-based identity (`did:ot:...`)
- Trust score as weighted components (identity, completion rate, dispute rate, description accuracy)
- Exponential decay (180-day window)
- Category-specific expertise scores

### 6. Federation
- Any server can run a PEP node
- Nodes sign listings, index verifies signatures
- gRPC sync between nodes
- Heartbeat monitoring, automatic revocation

## Architecture

```
+-------------------------------------------------------------+
|                    AI Agent Layer                           |
|  (Personal assistants, LLM agents, comparison bots)        |
+-----------------------------+-------------------------------+
                              | OpenTrade API (PEP Query)
                              v
+-------------------------------------------------------------+
|                   PEP Index Hub                             |
|  (Aggregates listings from all nodes, vector search)       |
+--------+----------+-----------+-------------------------------+
         |          |           |
         v          v           v
+-----------+ +-----------+ +-----------+
| Node A    | | Node B    | | Node C    |
| (Full     | | (Snow    | | (Local    |
|  marketplace) | board shop) | flea market) |
+-----------+ +-----------+ +-----------+
         |          |           |
         v          v           v
+-------------------------------------------------------------+
|           External Services Layer                           |
|  Logistics | Payments | Identity (DID) | AI/ML Verification |
+-------------------------------------------------------------+
```

## Go-to-Market Strategy

### Phase 1: Reference Node (0-6 months)
- Launch single node: `snow.opentradeprotocol.com` (snowboard niche)
- Perfect data schema, search API, escrow flow
- Publish OpenAPI spec
- Build agent SDK (Python + TypeScript)

### Phase 2: Open SDK (6-12 months)
- Release `@opentrade/agent-sdk`
- Invite niche marketplaces to run PEP nodes
- Free cross-posting tool

### Phase 3: PEP Index (12-18 months)
- Launch federated index
- Partner with AI agent platforms
- Protocol becomes industry standard

### Phase 4: Standard (18+ months)
- Monetization: escrow fees (1-3%), premium analytics
- Community-driven category schemas

## Technology Stack

| Layer | Technology |
|---|---|
| API Gateway | Kong / Envoy |
| Search | Meilisearch + Qdrant |
| Database | PostgreSQL + JSONB |
| Event Bus | Apache Kafka |
| Escrow | PostgreSQL state machine |
| Media | S3 + Cloudflare R2 |
| AI/ML | ONNX Runtime + CLIP |
| Federation | gRPC + Protobuf |
| Identity | did:web + Verifiable Credentials |

## Getting Started

### For AI Agent Developers

```bash
# Install the agent SDK
pip install @opentrade/agent-sdk

# Search across all federated nodes
import opentrade

client = opentrade.Client(api_key="your_key")
results = client.search(
    query="Jones Flagship 158",
    filters={"category": "snowboard", "condition": ["good", "like_new"]},
    buyer_location={"lat": 55.75, "lon": 37.61}
)

for listing in results:
    print(f"{listing.product.brand} {listing.product.model} - {listing.total_landed_cost.total} RUB")
```

### For Marketplace Operators

```bash
# Register your node
curl -X POST https://api.opentradeprotocol.com/v1/federation/register \
  -H "Content-Type: application/json" \
  -d '{
    "nodeId": "myshop.example.com",
    "nodePublicKey": "...",
    "capabilities": ["search", "escrow", "logistics"]
  }'
```

## Specification

The full protocol specification is in the `spec/` directory:

- **OpenAPI spec** (`spec/openapi/openapi.yaml`) — machine-readable API contract
- **JSON-LD context** (`spec/schemas/json-ld/context.jsonld`) — semantic schema
- **Protocol docs** (`spec/protocols/`) — federation, escrow, negotiation
- **Examples** (`spec/examples/`) — real data samples

## Contributing

We welcome contributions to:
- Category schemas (add new product types)
- Agent SDKs (more languages)
- Node implementations (new marketplaces)
- Documentation and examples

See [PLAN.md](PLAN.md) for the architecture decisions and roadmap.

## License

Apache 2.0 — the protocol is open, free, and governed by no single entity.

## Links

- **Website:** https://opentradeprotocol.com
- **API Docs:** https://api.opentradeprotocol.com/v1/docs
- **Protocol Spec:** https://opentradeprotocol.com/spec
- **GitHub:** https://github.com/open-trade-protocol

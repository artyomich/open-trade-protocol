# OpenTrade Protocol — Protocol Plan

## Overview

**OpenTrade Protocol** is an open standard for structured peer-to-peer commerce, optimized for AI agent consumption. It enables AI agents to search, negotiate, and complete transactions across federated marketplaces using a single machine-readable protocol.

**Vision:** Become the HTTP for P2P commerce. When AI agents make purchasing decisions, they need one protocol, not 50 different APIs.

**Analogy:** ActivityPub for social networks. Anyone can run a node. Agents speak one language.

---

## Decision: Adopting the Federated Architecture (Proposal 2)

We chose the federated model (Proposal 2) as the architectural foundation, combined with the pragmatic Go-to-Market strategy from Proposal 1.

### Why federation wins

| Criterion | Centralized (Proposal 1) | Federated (Proposal 2) |
|---|---|---|
| **Protocol adoption** | Requires convincing others to use your platform | Anyone can run a node; no gatekeeper |
| **Data quality** | Only your listings are structured | Network effect: more nodes = richer data |
| **AI agent appeal** | "One more marketplace API" | "One protocol for all commerce" |
| **Anti-fragility** | Single point of failure | No single point of control |
| **Standards path** | Must "open" later | Already open by design |
| **Trust model** | Platform-centric | Distributed trust graph |

### What we borrow from Proposal 1

- **Go-to-Market:** Start with one niche (snowboards), build a stellar reference implementation, then open
- **Total Cost endpoint:** Every listing must expose `total_landed_cost` for buyer location
- **AI-assisted listing:** CV + NLP to help sellers create perfect machine-readable listings
- **Schema-first design:** JSON Schema validation for every category
- **OpenAPI spec as contract:** AI agents read the spec and understand the API automatically

---

## Protocol Name: OpenTrade

- **Domain:** `opentradeprotocol.com` — available
- **GitHub:** `open-trade-protocol` — no conflicts
- **Why not Agora:** Oasis Protocol is a major blockchain project; naming conflict
- **Why not PEP:** Unfortunate political association; hard to brand
- **Why OpenTrade:** Descriptive, scalable, no conflicts, clear intent

---

## Core Protocol Components

### 1. Data Schema (JSON-LD + JSON Schema)

- Listings use JSON-LD with `pep:` prefix for semantic interoperability
- JSON Schema v2020-12 validation per category
- All critical fields typed: enums, numbers, references — no free text

### 2. Search & Discovery API

- `POST /v1/search` — structured + semantic search
- `POST /v1/search/semantic` — vector embedding search
- Results sorted by `relevance_score` and `total_landed_cost`
- Cursor-based pagination, `If-Modified-Since`, ETag support

### 3. Negotiation Protocol

- `POST /v1/listings/{id}/offers` — machine-readable offers
- AI agents can accept, reject, or counter-offer automatically
- Offers have TTL, signed by buyer DID

### 4. Escrow State Machine

```
[CREATED] → [FUNDED] → [SHIPPED] → [DELIVERED] → [INSPECTING] → [CONFIRMED] → [SETTLED]
                                                                    ↓
                                                              [DISPUTED]
                                                               ↓
                                                          [ARBITRATION]
```

- Each transition is a cryptographically signed event
- 48-hour inspection window
- PIN confirmation or AI photo verification

### 5. Trust Graph

- DID-based identity (`did:pep:...`)
- Trust score as weighted components:
  - `identity_verification`
  - `transaction_completion`
  - `dispute_resolution`
  - `description_accuracy` (AI-computed from photo comparison)
  - `shipping_speed`
- Exponential decay (180-day window)

### 6. Federation Protocol

- `POST /v1/federation/announce` — nodes publish listings to the index
- gRPC + Protobuf for node-to-node sync
- PEP Index aggregates across all nodes
- Nodes sign their listings; index verifies signatures

---

## Go-to-Market Strategy

### Phase 1: Reference Node (0–6 months)

- Launch single node: `snow.opentrades.io` (snowboard niche)
- Perfect the data schema, search API, and escrow flow
- Publish OpenAPI spec
- Build agent SDK (Python + TypeScript)
- Create AI-assisted listing tool (upload photos → structured listing)

### Phase 2: Open SDK (6–12 months)

- Release `@opentrade/agent-sdk` for Python and TypeScript
- Documentation: "Connect your marketplace to AI agents in 5 minutes"
- Invite 3–5 niche marketplaces to run PEP nodes
- Free cross-posting tool: publish to your site + OpenTrade simultaneously

### Phase 3: PEP Index (12–18 months)

- Launch federated index
- Partner with 2–3 AI agent platforms (Yandex Alice, GigaChat, OpenAI Operator)
- AI agents treat OpenTrade as a primary data source

### Phase 4: Standard (18+ months)

- Protocol becomes industry standard
- Monetization: PEP Escrow fees (1–3%), premium agent analytics
- Category schemas contributed by community

---

## Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| API Gateway | Kong / Envoy | Rate limiting, agent auth, gRPC transcoding |
| Search | Meilisearch + Qdrant | Structured filters + vector search |
| Database | PostgreSQL + JSONB | Flexible schema with validation |
| Event Bus | Apache Kafka | Escrow events, federation sync, webhooks |
| Escrow | PostgreSQL state machine → L2 blockchain | Start simple, evolve to transparent smart contracts |
| Media | S3 + Cloudflare R2 + imgproxy | AVIF/WebP on-the-fly, CDN |
| AI/ML | ONNX Runtime + CLIP | Photo verification, listing generation, fraud detection |
| Federation | gRPC + Protobuf | Fast node-to-node sync |
| Identity | did:web + Verifiable Credentials | W3C standard, Gosuslugy compatibility |

---

## Naming Conventions

- **Protocol:** OpenTrade Protocol
- **Specification prefix:** `ot:` (e.g., `ot:Listing`, `ot:TrustScore`)
- **Context URL:** `https://opentrades.io/v1/context.jsonld`
- **API base:** `https://api.opentrades.io/v1/`
- **Agent SDK:** `@opentrade/agent-sdk`
- **Domain:** `opentrades.io` (short, memorable)

---

## Key Design Decisions

1. **JSON-LD over raw JSON** — Schema.org compatibility means Google, Bing, and other agents already understand our semantics
2. **DID over email/phone** — Privacy-preserving identity, verifiable credentials
3. **Federated over centralized** — Protocol adoption requires no gatekeeper
4. **Negotiation as first-class citizen** — AI agents must be able to haggle programmatically
5. **Trust as computed data** — Not star ratings; weighted, decayed, AI-verified metrics
6. **Total cost always** — Every price endpoint returns `total_landed_cost` for buyer location

---

## Open Questions

- [ ] Escrow: centralized (Postgres) vs. L2 blockchain (Polygon/Arbitrum)? Decision: start centralized, design for migration
- [ ] Federation discovery: DNS-based (like ActivityPub) vs. central registry? Decision: hybrid — central PEP Index for discovery, DNS for fallback
- [ ] Currency support: fiat only initially, or crypto escrow from day one? Decision: fiat only, crypto escrow as Phase 2
- [ ] Dispute resolution: platform-mediated vs. decentralized arbitration? Decision: platform-mediated first, DAO arbitration later
- [ ] Category schema governance: who maintains category schemas? Decision: community-driven via GitHub, OpenTrade Foundation for final approval

---

## Next Steps

1. [ ] Draft full OpenAPI spec (`spec/openapi/openapi.yaml`)
2. [ ] Define JSON-LD context (`spec/schemas/json-ld/context.jsonld`)
3. [ ] Create product listing examples (`spec/examples/product-listing/`)
4. [ ] Write architecture diagrams (`assets/diagrams/`)
5. [ ] Build reference implementation MVP (snowboard node)
6. [ ] Publish agent SDK alpha
7. [ ] Open-source the protocol spec on GitHub

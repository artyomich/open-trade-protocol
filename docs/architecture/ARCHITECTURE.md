# OpenTrade Protocol Architecture

## System Architecture

```
                    ┌─────────────────────────────────────────┐
                    │         AI Agent Layer                  │
                    │  (Personal assistants, LLM bots,        │
                    │   comparison tools, autonomous buyers)  │
                    └─────────────────┬───────────────────────┘
                                      │ OpenTrade API
                                      │ (HTTPS + gRPC)
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                        API Gateway                              │
│  • Rate limiting (per API key / DID)                            │
│  • Authentication (API keys, DID JWT, Node keys)               │
│  • Request routing & SSL termination                            │
│  • OpenAPI spec served at /openapi.json                         │
└───────────────────────┬─────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Search       │ │ Product      │ │ Trust /      │
│ Service      │ │ Service      │ │ Reputation   │
│              │ │              │ │ Service      │
│ Meilisearch  │ │ PostgreSQL   │ │ PostgreSQL   │
│ + Qdrant     │ │ + JSONB      │ │ + Redis      │
│              │ │              │ │              │
│ • Full-text  │ │ • Listing    │ │ • Trust      │
│ • Faceted    │ │   storage    │ │   graph      │
│ • Geo search │ │ • Category   │ │ • Ratings    │
│ • Vector     │ │   schemas    │ │ • History    │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                 │
       └────────────────┼─────────────────┘
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Event Bus (Kafka)                          │
│  Topics:                                                        │
│  • listing.created / listing.updated                            │
│  • escrow.status_changed                                        │
│  • trust.score_updated                                          │
│  • federation.sync                                              │
└───────┬───────────────┬────────────────┬───────────────────────┘
        ▼               ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌─────────────────────────────┐
│ Escrow /     │ │ Logistics    │ │ AI / ML Service             │
│ Payment      │ │ Service      │ │                             │
│ Service      │ │              │ │ • CV: photo verification    │
│              │ │ Integrations:│ │   (condition, defect)       │
│ • Hold funds │ │ • CDEK       │ │ • NLP: text -> structured   │
│ • PIN confirm│ │ • Russian    │ │   attributes                  │
│ • Dispute    │ │   Post      │ │ • Price suggestion            │
│ • Refund     │ │ • Yandex     │ │ • Fraud detection             │
│ • Payout     │ │   Delivery   │ │ • Embedding generation        │
└──────┬───────┘ └──────┬───────┘ └─────────────────────────────┘
       │                │
       ▼                ▼
┌──────────────┐ ┌──────────────┐
│ Media /      │ │ Notification │
│ Storage      │ │ Service      │
│              │ │              │
│ S3 + R2 +    │ │ Push, SMS,   │
│ imgproxy     │ │ Email, Webhook│
│ AVIF/WebP    │ │              │
└──────────────┘ └──────────────┘
```

## Service Details

### API Gateway
- **Tech:** Kong or Envoy
- **Responsibilities:**
  - Rate limiting per API key / DID
  - Authentication (API keys for agents, DID JWT for authenticated actions, Node keys for federation)
  - Request routing to backend services
  - SSL/TLS termination
  - OpenAPI spec serving (`/openapi.json`)
  - Request/response logging for analytics

### Search Service
- **Tech:** Meilisearch + Qdrant
- **Responsibilities:**
  - Full-text search with typo tolerance
  - Faceted search (category, brand, condition, price range)
  - Geo-search (radius-based filtering)
  - Vector search for semantic queries
  - Result ranking by relevance_score and total_landed_cost
  - Cursor-based pagination
  - ETag support for caching

### Product Service
- **Tech:** PostgreSQL + JSONB
- **Responsibilities:**
  - Listing CRUD operations
  - JSON Schema validation per category
  - Category schema management
  - Media URL resolution
  - Price history tracking
  - Bulk listing export for indexing

### Trust / Reputation Service
- **Tech:** PostgreSQL + Redis
- **Responsibilities:**
  - Trust score computation (weighted components)
  - Trust graph storage
  - Category expertise tracking
  - Dispute rate calculation
  - Exponential decay (180-day window)
  - Cached scores in Redis for fast lookup

### Escrow / Payment Service
- **Tech:** PostgreSQL (state machine)
- **Responsibilities:**
  - Escrow state machine management
  - Fund holding and release
  - PIN code generation and verification
  - Dispute workflow management
  - Payout scheduling
  - Integration with payment gateways (Stripe, etc.)
  - Webhook delivery for state transitions

### Logistics Service
- **Tech:** Microservice with external API integrations
- **Responsibilities:**
  - Shipping cost calculation
  - Carrier integration (CDEK, Russian Post, Yandex Delivery)
  - Tracking number management
  - Delivery estimation
  - Insurance cost calculation
  - Total landed cost computation

### AI / ML Service
- **Tech:** ONNX Runtime + CLIP
- **Responsibilities:**
  - Photo verification (condition, defects)
  - Listing generation from photos
  - Price suggestion based on market data
  - Fraud detection
  - Embedding generation for semantic search
  - AI confidence scoring

### Media / Storage Service
- **Tech:** S3 + Cloudflare R2 + imgproxy
- **Responsibilities:**
  - Image/video storage
  - On-the-fly format conversion (AVIF, WebP)
  - Thumbnail generation
  - CDN distribution
  - Image verification (hash-based dedup)

### Notification Service
- **Tech:** Microservice with multiple delivery channels
- **Responsibilities:**
  - Push notifications
  - SMS delivery
  - Email delivery
  - Webhook delivery to AI agents
  - Retry logic with exponential backoff
  - Dead letter queue for failed deliveries

## Data Flow: Search

```
AI Agent              API Gateway          Search Service        Product Service
    |                       |                      |                     |
    |--- POST /search ----->|                      |                     |
    |                       |--- query parse ------>|                     |
    |                       |                      |                     |
    |                       |                      |--- search Meilisearch|
    |                       |                      |<-- results ----------|
    |                       |                      |                     |
    |                       |                      |--- enrich with      |
    |                       |                      |   total_cost        |
    |                       |                      |   trust_score       |
    |                       |                      |<-- enriched --------|
    |                       |<-- results -----------|                     |
    |<-- results -----------|                      |                     |
```

## Data Flow: Escrow

```
Buyer Agent       API Gateway      Escrow Service     Payment Gateway
    |                  |                  |                    |
    |--- create escrow->|                 |                    |
    |                  |--- validate ---->|                    |
    |                  |                  |--- create contract |
    |                  |                  |<-- escrow_id ------|
    |                  |<-- payment_url --|                    |
    |<-- payment_url -|                  |                    |
    |                  |                  |                    |
    |--- pay --------->|                  |                    |
    |                  |                  |                    |--- initiate payment
    |                  |                  |<--- payment_confirmed
    |                  |                  |                    |
    |                  |                  |--- update status   |
    |                  |                  |   to FUNDED        |
    |                  |                  |--- notify seller  |
    |                  |                  |<-- escrow created |
    |<-- escrow ------|                  |                    |
```

## Infrastructure

### Deployment
- **Cloud:** AWS or equivalent
- **Container:** Docker + Kubernetes
- **CI/CD:** GitHub Actions
- **Monitoring:** Prometheus + Grafana
- **Logging:** ELK stack
- **Tracing:** OpenTelemetry

### Scaling
- Search service: horizontal scale with Meilisearch replication
- Product service: read replicas for PostgreSQL
- Event bus: Kafka partitioning by category
- CDN: Cloudflare for media and static assets
- Cache: Redis cluster for trust scores and frequently accessed listings

### Security
- TLS 1.3 for all traffic
- API key rotation (90-day expiry)
- DID JWT for authenticated actions
- Node key rotation (compromise detection)
- Rate limiting with sliding window
- DDoS protection via CDN
- Data encryption at rest (AES-256)
- Audit logging for all escrow operations

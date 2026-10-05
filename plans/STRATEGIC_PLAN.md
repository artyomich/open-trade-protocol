# OpenTrade Protocol — Detailed Strategic Plan & Architecture

**Version:** 1.0  
**Date:** 2026-10-05  
**Status:** Draft for Review

---

## TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [Repository Structure Strategy](#2-repository-structure-strategy)
3. [Hugo Website Strategy](#3-hugo-website-strategy)
4. [Phased Development Roadmap](#4-phased-development-roadmap)
5. [Open-Source Best Practices](#5-open-source-best-practices)
6. [Architecture Evolution](#6-architecture-evolution)
7. [Risk Matrix](#7-risk-matrix)
8. [Success Criteria](#8-success-criteria)

---

## 1. EXECUTIVE SUMMARY

This document provides a detailed strategic plan for the evolution of **OpenTrade Protocol** from its current state (a single repository with protocol specs and reference implementation) into a mature, well-governed open-source ecosystem capable of supporting widespread adoption by marketplace operators and AI agent developers.

### Key Decisions

| Decision | Recommendation | Rationale |
|----------|---------------|-----------|
| Repo Strategy | **Multi-repo under organization** | Clear separation of concerns; each component can evolve independently with its own release cycle |
| Website | **Dedicated Hugo repo** | Hugo is the de-facto standard for open-source project sites; GitPages CDN is free and reliable |
| Governance | **Organization-first** | All repos under `open-trade-protocol` org; personal fork only for initial development |
| Protocol Versioning | **Semantic versioning with RFC-style proposals** | Industry standard for protocol evolution |
| License | **Apache 2.0 for code, CC-BY 4.0 for docs** | Allows commercial use, patents, and derivatives |

---

## 2. REPOSITORY STRUCTURE STRATEGY

### 2.1. Recommendation: Multi-Repo Under Organization

**Adopt a multi-repository strategy** with all primary repos under the `open-trade-protocol` GitHub organization. This approach provides:

- **Clear ownership boundaries** — Each repo has a focused purpose and maintainers
- **Independent release cycles** — Protocol specs can version independently from reference implementations
- **Targeted contributions** — Contributors work on specific areas without navigating unrelated code
- **Granular CI/CD** — Each repo has tailored build/test/deploy pipelines
- **Reduced attack surface** — Security issues in one component don't compromise the entire codebase

### 2.2. Proposed Repository Inventory

#### Core Protocol Repositories (Under `open-trade-protocol` org)

| Repository | Purpose | Tech | Initial Status |
|------------|---------|------|----------------|
| [`open-trade-protocol/spec`](https://github.com/open-trade-protocol/spec) | **Protocol specifications** — OpenAPI, JSON-LD, JSON Schema, protocol documents, examples | YAML, JSON, Markdown | Migrate from current `spec/` |
| [`open-trade-protocol/agent-sdk-python`](https://github.com/open-trade-protocol/agent-sdk-python) | Python SDK for AI agents to interact with OpenTrade nodes | Python 3.12+, Pydantic | Migrate from `reference-impl/agent-sdk/python/` |
| [`open-trade-protocol/agent-sdk-typescript`](https://github.com/open-trade-protocol/agent-sdk-typescript) | TypeScript SDK for AI agents | TypeScript 5+, Node.js 20+ | Migrate from `reference-impl/agent-sdk/typescript/` |
| [`open-trade-protocol/pep-node`](https://github.com/open-trade-protocol/pep-node) | Reference PEP node implementation (Python FastAPI) | Python 3.12+, FastAPI, PostgreSQL | Migrate from `reference-impl/peer-node/` |
| [`open-trade-protocol/pep-index`](https://github.com/open-trade-protocol/pep-index) | Federated index service — aggregates listings from all PEP nodes | Python 3.12+, FastAPI, Meilisearch, Qdrant | Migrate from `reference-impl/pep-index/` |
| [`open-trade-protocol/escrow-service`](https://github.com/open-trade-protocol/escrow-service) | Escrow/payment service implementation | Python 3.12+, PostgreSQL, Stripe SDK | Migrate from `reference-impl/escrow-service/` |
| [`open-trade-protocol/website`](https://github.com/open-trade-protocol/website) | Hugo-based project website and documentation site | Hugo, Markdown, CSS | **NEW** |
| [`open-trade-protocol/trust-service`](https://github.com/open-trade-protocol/trust-service) | Trust/reputation service implementation | Python 3.12+, PostgreSQL, Redis | Migrate from `reference-impl/trust-service/` |
| [`open-trade-protocol/search-service`](https://github.com/open-trade-protocol/search-service) | Search service with Meilisearch + vector search | Python 3.12+, Meilisearch, Qdrant | Migrate from `reference-impl/search-service/` |

#### Infrastructure & Operations Repositories

| Repository | Purpose | Tech | Initial Status |
|------------|---------|------|----------------|
| [`open-trade-protocol/infrastructure`](https://github.com/open-trade-protocol/infrastructure) | Terraform, Kubernetes manifests, Docker Compose for deployment | HCL, YAML, Docker | **NEW** |
| [`open-trade-protocol/monitoring`](https://github.com/open-trade-protocol/monitoring) | Prometheus, Grafana, alerting rules | YAML, Go (PromQL) | **NEW** |
| [`open-trade-protocol/ci-tools`](https://github.com/open-trade-protocol/ci-tools) | Shared CI/CD workflows, linting, validation scripts | YAML (GitHub Actions), Python, Bash | **NEW** |

#### Community & Governance Repositories

| Repository | Purpose | Tech | Initial Status |
|------------|---------|------|----------------|
| [`open-trade-protocol/foundation`](https://github.com/open-trade-protocol/foundation) | RFC proposals, governance documents, meeting notes | Markdown | **NEW** |
| [`open-trade-protocol/awesome-opentrade`](https://github.com/open-trade-protocol/awesome-opentrade) | Curated list of community contributions, integrations, nodes | Markdown | **NEW** |

### 2.3. Repository Migration Map

```
Current Location                          →  Target Repository
─────────────────────────────────────────────────────────────────────
spec/                                   →  open-trade-protocol/spec
  ├── openapi/openapi.yaml              →  spec/openapi/openapi.yaml
  ├── schemas/json-ld/                  →  spec/contexts/json-ld/
  ├── schemas/categories/               →  spec/schemas/categories/
  ├── protocols/                        →  spec/protocols/
  └── examples/                         →  spec/examples/

reference-impl/agent-sdk/python/        →  agent-sdk-python/
reference-impl/agent-sdk/typescript/    →  agent-sdk-typescript/
reference-impl/peer-node/               →  pep-node/
reference-impl/pep-index/               →  pep-index/
reference-impl/escrow-service/          →  escrow-service/
reference-impl/trust-service/           →  trust-service/
reference-impl/search-service/          →  search-service/
reference-impl/product-service/         →  merged into pep-node/
reference-impl/api-gateway/             →  infrastructure/ (configs only)
reference-impl/federation/              →  merged into pep-node/
```

### 2.4. Monorepo vs Multirepo Decision Matrix

| Criterion | Monorepo | Multirepo (RECOMMENDED) |
|-----------|----------|-------------------------|
| Protocol spec isolation | Hard to isolate | Clean boundary |
| SDK release frequency | Blocked by other changes | Independent releases |
| Contributor focus | Must understand everything | Focus on specific area |
| Dependency management | Shared, simple | Per-repo, more complex |
| CI/CD complexity | Single pipeline | Per-repo pipelines |
| Security boundaries | Shared blast radius | Isolated blast radius |
| Standards body path | Requires restructuring | Already structured |
| Community contributions | Can be overwhelming | Targeted, manageable |

**Verdict: Multi-repo is recommended** because:
1. Protocol specifications must evolve independently from implementations
2. SDK releases need their own versioning cadence (semver)
3. Different components have different security requirements
4. The target audience (external marketplace operators) benefits from clean separation between "the protocol" and "our implementation"

### 2.5. Protocol vs Implementation Separation

```
┌─────────────────────────────────────────────────────────────────────┐
│                    open-trade-protocol/spec                        │
│  (Protocol — what any implementation MUST follow)                  │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │ OpenAPI      │  │ JSON-LD      │  │ Protocol Docs            │ │
│  │ Contracts    │  │ Contexts     │  │ (RFC-style)              │ │
│  │              │  │              │  │                          │ │
│  │ Search API   │  │ ot:Listing   │  │ Federation Protocol      │ │
│  │ Escrow API   │  │ ot:Offer     │  │ Escrow Protocol          │ │
│  │ Negotiation  │  │ ot:Escrow    │  │ Negotiation Protocol     │ │
│  │ API          │  │ ot:TrustScore│  │                          │ │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘ │
│                                                                     │
│  ALL external partners implement against THIS layer                 │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│              Reference Implementations (examples, not required)     │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐ │
│  │ pep-node     │  │ pep-index    │  │ escrow-service           │ │
│  │ (Python)     │  │ (Python)     │  │ (Python)                 │ │
│  │              │  │              │  │                          │ │
│  │ "Reference   │  │ "Reference   │  │ "Reference               │ │
│  │  implementation"  implementation"  escrow impl"              │ │
│  └──────────────┘  └──────────────┘  └──────────────────────────┘ │
│                                                                     │
│  These prove the protocol works but are NOT the protocol            │
└─────────────────────────────────────────────────────────────────────┘
```

**Critical principle:** Any marketplace operator should be able to implement an OpenTrade-compliant node in any language/framework using ONLY the `spec/` repository. The reference implementations serve as proof-of-concept and starting templates.

---

## 3. HUGO WEBSITE STRATEGY

### 3.1. Repository: `open-trade-protocol/website`

A dedicated Hugo site repository, separate from all protocol and implementation repos.

### 3.2. Hugo Site Structure

```
website/
├── hugo.toml                          # Hugo configuration
├── assets/
│   ├── css/
│   │   ├── main.css                   # Primary styles
│   │   ├── syntax-highlighting.css    # Code block styles
│   │   └── print.css                  # Print-specific styles
│   ├── icons/
│   │   ├── favicon.svg
│   │   ├── og-image.png               # Open Graph image
│   │   └── logo.svg
│   └── js/
│       ├── search.js                  # Client-side search
│       └── mermaid-loader.js          # Mermaid diagram rendering
├── content/
│   ├── _index.md                      # Homepage
│   ├── docs/
│   │   ├── _index.md
│   │   ├── getting-started/
│   │   │   ├── _index.md
│   │   │   ├── introduction.md
│   │   │   ├── quickstart.md
│   │   │   └── architecture.md
│   │   ├── protocol/
│   │   │   ├── _index.md
│   │   │   ├── search-api.md
│   │   │   ├── escrow-protocol.md
│   │   │   ├── negotiation-protocol.md
│   │   │   ├── federation-protocol.md
│   │   │   ├── trust-model.md
│   │   │   └── identity-did.md
│   │   ├── sdk/
│   │   │   ├── _index.md
│   │   │   ├── python/
│   │   │   │   ├── _index.md
│   │   │   │   ├── installation.md
│   │   │   │   ├── search.md
│   │   │   │   ├── negotiation.md
│   │   │   │   └── escrow.md
│   │   │   └── typescript/
│   │   │       ├── _index.md
│   │   │       ├── installation.md
│   │   │       ├── search.md
│   │   │       ├── negotiation.md
│   │   │       └── escrow.md
│   │   ├── node-operator/
│   │   │   ├── _index.md
│   │   │   ├── deployment.md
│   │   │   ├── configuration.md
│   │   │   ├── federation-setup.md
│   │   │   └── monitoring.md
│   │   ├── governance/
│   │   │   ├── _index.md
│   │   │   ├── contributing.md
│   │   │   ├── rfc-process.md
│   │   │   ├── code-of-conduct.md
│   │   │   └── licensing.md
│   │   └── roadmap.md
│   ├── community/
│   │   ├── _index.md
│   │   ├── members.md
│   │   ├── events.md
│   │   └── blog/
│   │       ├── _index.md
│   │       └── 2026-10-05-strategic-plan.md
│   └── about/
│       ├── _index.md
│       ├── mission.md
│       ├── team.md
│       └── contact.md
├── layouts/
│   ├── _default/
│   │   ├── baseof.html
│   │   ├── list.html
│   │   ├── single.html
│   │   ├── docs.html                # Custom layout for docs section
│   │   └── taxonomy.html
│   ├── partials/
│   │   ├── header.html
│   │   ├── footer.html
│   │   ├── sidebar.html
│   │   ├── search.html
│   │   ├── schema-markup.html        # JSON-LD structured data
│   │   └── mermaid-diagram.html
│   ├── docs/
│   │   └── list.html
│   └── index.html
├── data/
│   ├── protocol-versions.yaml         # Protocol version metadata
│   ├── sdk-versions.yaml              # SDK version info
│   └── partners.yaml                  # Partner nodes
├── static/
│   ├── diagrams/
│   │   ├── architecture/
│   │   │   ├── system-overview.svg
│   │   │   ├── data-flow-search.svg
│   │   │   └── data-flow-escrow.svg
│   │   └── protocols/
│   │       ├── escrow-state-machine.svg
│   │       └── federation-sync.svg
│   └── brand/
│       ├── logo-dark.svg
│       ├── logo-light.svg
│       └── style-guide.pdf
├── themes/
│   └── opentrade/                    # Custom theme (or use docsy)
├── scripts/
│   ├── validate-specs.sh              # Validate OpenAPI/JSON-LD
│   ├── generate-api-docs.sh           # Generate API docs from spec
│   └── sync-specs.sh                  # Sync specs from spec/ repo
└── README.md
```

### 3.3. Hugo Configuration (`hugo.toml`)

```toml
baseURL = 'https://opentradeprotocol.com/'
languageCode = 'en-us'
title = 'OpenTrade Protocol'
theme = 'opentrade'

# Internationalization (future)
defaultContentLanguage = 'en'
defaultContentLanguageInSubdir = false

# Docsy-like docs structure
[outputs]
  home = ['HTML', 'RSS', 'JSON']
  section = ['HTML', 'RSS', 'JSON']

# Markup configuration
[markup]
  [markup.goldmark]
    [markup.goldmark.renderer]
      unsafe = true
  [markup.highlight]
    style = 'github-dark'
    lineNumbers = true
  [markup.tableOfContents]
    startLevel = 2
    endLevel = 4
    ordered = false

# Menus
[[menu.main]]
  identifier = 'docs'
  name = 'Docs'
  url = '/docs/'
  weight = 1

[[menu.main]]
  identifier = 'protocol'
  name = 'Protocol'
  url = '/docs/protocol/'
  weight = 2

[[menu.main]]
  identifier = 'sdk'
  name = 'SDK'
  url = '/docs/sdk/'
  weight = 3

[[menu.main]]
  identifier = 'community'
  name = 'Community'
  url = '/community/'
  weight = 4

[[menu.main]]
  identifier = 'github'
  name = 'GitHub'
  url = 'https://github.com/open-trade-protocol'
  weight = 5
  post = '<i class="fab fa-github"></i>'

# Params
[params]
  description = 'Open protocol for structured peer-to-peer commerce, optimized for AI agent consumption.'
  github_repo = 'https://github.com/open-trade-protocol'
  github_project_repo = 'https://github.com/open-trade-protocol'
  offlineNote = 'Docs available offline via service worker'
  version = '0.1.0'
  commit = 'HEAD'
  flavor = 'bootstrap'
  disable_og = false
  disable_analytics = false
  disable_seo_photos = false
```

### 3.4. CI/CD Pipeline for Website

```yaml
# .github/workflows/deploy-website.yml
name: Deploy Website

on:
  push:
    branches: [main]
    paths:
      - 'website/**'
  pull_request:
    paths:
      - 'website/**'

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: true

jobs:
  # Build job
  build:
    runs-on: ubuntu-latest
    env:
      HUGO_VERSION: 0.136.0
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Checkout specs repo
        uses: actions/checkout@v4
        with:
          repository: open-trade-protocol/spec
          path: specs

      - name: Sync specs to website
        run: |
          mkdir -p website/content/spec
          cp -r specs/openapi/*.yaml website/content/spec/openapi/
          cp -r specs/protocols/*.md website/content/spec/protocols/
          cp -r specs/schemas/*.json website/content/spec/schemas/

      - name: Setup Hugo
        uses: peaceiris/actions-hugo@v3
        with:
          hugo-version: ${{ env.HUGO_VERSION }}
          extended: true

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20

      - name: Build
        run: |
          cd website
          hugo --minify --gc --cleanDestinationDir
        env:
          HUGO_ENVIRONMENT: production

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: website/public

  # Deploy job
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 3.5. Domain & DNS Configuration

```
DNS Records for opentradeprotocol.com:

┌─────────────────────────────────────────────────────────────────────┐
│  DNS Configuration                                                  │
│                                                                     │
│  Type    Name              Value                        Purpose   │
│  ──      ──                ────                        ───────     │
│  CNAME   www             opentrade-protocol.github.io  GitHub Pages│
│  CNAME   docs           opentrade-protocol.github.io  Docs only   │
│  CNAME   api            (future API gateway)           API docs    │
│  A       @               185.199.108.153              Root (redirect)
│  A       @               185.199.109.153              Root (redirect)
│  A       @               185.199.110.153              Root (redirect)
│  A       @               185.199.111.153              Root (redirect)
│  TXT     @               "v=spf1 include:github.com ~all"  SPF     │
│  TXT     _dmarc           "v=DMARC1; p=none"          DMARC       │
│  TLSA    _443._tcp       (for DANE)                   Security    │
└─────────────────────────────────────────────────────────────────────┘
```

### 3.6. Content Strategy by Audience

| Audience | Primary Content | Secondary Content |
|----------|----------------|-------------------|
| **AI Agent Developers** | SDK docs, API reference, code examples, integration guides | Protocol specs, architecture diagrams |
| **Marketplace Operators** | Node deployment guide, federation setup, configuration reference | Trust model, escrow integration |
| **Decision Makers** | Architecture overview, GTM strategy, case studies, ROI | Technical deep-dives (linked) |
| **Contributors** | Contributing guide, RFC process, coding standards | All technical docs |

### 3.7. SEO & Discoverability

- **JSON-LD structured data** on every page (SoftwareSource, Documentation, Article schemas)
- **Sitemap.xml** auto-generated by Hugo
- **Open Graph** and **Twitter Card** meta tags
- **robots.txt** allowing all crawler paths
- **Canonical URLs** to prevent duplicate content issues
- **RSS feed** for blog and changelog

---

## 4. PHASED DEVELOPMENT ROADMAP

### 4.1. Phase 1: Foundation (Months 1-3)

**Theme:** Repository restructuring, website launch, protocol stabilization

#### Month 1: Repository & Infrastructure Setup

| # | Task | Repository | Owner | Deliverable |
|---|------|-----------|-------|-------------|
| 1.1 | Create organization repos | GitHub | Admin | 9 repos created under `open-trade-protocol` org |
| 1.2 | Migrate `spec/` to `spec/` repo | spec | Admin | Clean protocol spec repo with CI validation |
| 1.3 | Create `ci-tools` repo | ci-tools | Admin | Shared linting, spec validation workflows |
| 1.4 | Set up `infrastructure` repo | infrastructure | Admin | Terraform for AWS, Docker Compose for local dev |
| 1.5 | Create `foundation` repo | foundation | Admin | RFC template, governance docs, meeting notes |
| 1.6 | Set up CI/CD for spec repo | spec | Admin | Auto-validate OpenAPI, JSON-LD, JSON Schema on PR |

**Month 1 Milestones:**
- [ ] All repos created under `open-trade-protocol` org
- [ ] `spec/` repo with automated validation pipeline
- [ ] `ci-tools` repo with shared workflows
- [ ] Organization settings configured (SECURITY.md, CODEOWNERS, etc.)

#### Month 2: Website & Documentation

| # | Task | Repository | Owner | Deliverable |
|---|------|-----------|-------|-------------|
| 2.1 | Create `website` repo with Hugo | website | Admin | Hugo site scaffolded with theme |
| 2.2 | Implement custom theme | website | Designer | Brand-aligned Hugo theme |
| 2.3 | Write core documentation | website | Tech Writer | Getting started, architecture, protocol overview |
| 2.4 | Set up CI/CD for site | website | Admin | Auto-deploy to GitHub Pages on merge |
| 2.5 | Configure domain DNS | DNS | Admin | opentradeprotocol.com → GitHub Pages |
| 2.6 | Write migration guides | foundation | Admin | How to contribute, how to implement |

**Month 2 Milestones:**
- [ ] opentradeprotocol.com live with Hugo site
- [ ] Full documentation published (getting started, architecture, protocol overview)
- [ ] CI/CD auto-deploys on content changes
- [ ] SSL certificate configured

#### Month 3: Protocol Stabilization

| # | Task | Repository | Owner | Deliverable |
|---|------|-----------|-------|-------------|
| 3.1 | Finalize OpenAPI spec v1.0 | spec | Protocol Lead | OpenAPI 3.1.0, validated, published |
| 3.2 | Finalize JSON-LD context | spec | Protocol Lead | Stable context with all types defined |
| 3.3 | Add category schemas | spec | Schema Lead | Snowboard, shoes, watches categories |
| 3.4 | Write RFC process | foundation | Governance | Formal RFC proposal/acceptance process |
| 3.5 | Create first RFCs | foundation | Protocol Lead | RFC-001 (escrow finalization), RFC-002 (category governance) |
| 3.6 | Set up CODEOWNERS | All repos | Admin | Review requirements per directory |

**Month 3 Milestones:**
- [ ] OpenAPI spec v1.0 (feature complete for MVP)
- [ ] 3 category schemas published
- [ ] RFC process documented and first RFCs submitted
- [ ] CODEOWNERS configured in all repos

---

### 4.2. Phase 2: Reference Implementation Hardening (Months 4-6)

**Theme:** Production-ready reference node, SDK stabilization, first external adopters

#### Month 4: Node & SDK Improvements

| # | Task | Repository | Owner | Deliverable |
|---|------|-----------|-------|-------------|
| 4.1 | Harden `pep-node` for production | pep-node | Lead Dev | Health checks, graceful shutdown, metrics |
| 4.2 | Add integration tests | pep-node | QA | E2E tests for search, escrow, federation |
| 4.3 | Release agent-sdk-python v0.1 | agent-sdk-python | SDK Lead | PyPI package with docs |
| 4.4 | Release agent-sdk-typescript v0.1 | agent-sdk-typescript | SDK Lead | npm package with docs |
| 4.5 | Write SDK quickstart guides | website | Tech Writer | "Hello World" in Python and TypeScript |
| 4.6 | Set up monitoring stack | monitoring | DevOps | Prometheus + Grafana for reference node |

#### Month 5: Federation & Escrow

| # | Task | Repository | Owner | Deliverable |
|---|------|-----------|-------|-------------|
| 5.1 | Finalize federation protocol | spec | Protocol Lead | RFC-accepted federation spec |
| 5.2 | Implement escrow payment flow | escrow-service | Lead Dev | Stripe integration, state machine |
| 5.3 | Add trust service to pep-node | trust-service | Dev | Trust score computation |
| 5.4 | Write node operator guide | website | Tech Writer | Deployment, configuration, monitoring |
| 5.5 | Create onboarding flow | pep-node | Dev | Automated node registration |
| 5.6 | Security audit of escrow | escrow-service | External | Third-party review |

#### Month 6: First External Adopters

| # | Task | Repository | Owner | Deliverable |
|---|------|-----------|-------|-------------|
| 6.1 | Recruit 3 beta partners | Foundation | PM | MOUs with 3 marketplace operators |
| 6.2 | Create partner onboarding kit | foundation | PM | Setup guide, support channel, SLA |
| 6.3 | Host first community call | foundation | PM | Recorded meeting, action items |
| 6.4 | Release pep-node v0.2 | pep-node | Lead Dev | Docker images, Helm chart |
| 6.5 | Add analytics dashboard | pep-index | Dev | Node health, listing stats, federation metrics |
| 6.6 | Write case study | website | Tech Writer | Snowboard node operational metrics |

**Phase 2 Milestones:**
- [ ] pep-node production-ready (99.9% uptime target)
- [ ] Both SDKs published (v0.1)
- [ ] 3 beta partners onboarded
- [ ] Security audit completed
- [ ] First community call held

---

### 4.3. Phase 3: Community Growth (Months 7-9)

**Theme:** SDK maturity, protocol extensions, growing adopter base

| # | Task | Repository | Owner | Deliverable |
|---|------|-----------|-------|-------------|
| 7.1 | Release agent-sdk-python v0.2 | agent-sdk-python | SDK Lead | Webhooks, batch operations, async |
| 7.2 | Release agent-sdk-typescript v0.2 | agent-sdk-typescript | SDK Lead | Same feature parity as Python |
| 7.3 | Add Go SDK (community) | agent-sdk-go | Community | Go client library |
| 7.4 | RFC-accepted trust model | spec | Protocol Lead | RFC-003 (trust score algorithm) |
| 7.5 | Add multi-currency support | spec | Protocol Lead | RFC-004 (currency extension) |
| 7.6 | Create API reference docs | website | Tech Writer | Auto-generated from OpenAPI |
| 7.7 | Host first hackathon | foundation | PM | AI agent builders using OpenTrade |
| 7.8 | Add partner nodes dashboard | website | Dev | Live list of federated nodes |

**Phase 3 Milestones:**
- [ ] SDKs v0.2 with webhook support
- [ ] Go SDK community contribution
- [ ] 2 RFCs accepted
- [ ] First hackathon completed
- [ ] 10+ registered PEP nodes

---

### 4.4. Phase 4: Protocol Maturity (Months 10-12)

**Theme:** v1.0 release, enterprise readiness, governance formalization

| # | Task | Repository | Owner | Deliverable |
|---|------|-----------|-------|-------------|
| 10.1 | Protocol v1.0 spec freeze | spec | Protocol Lead | Stable API, no breaking changes |
| 10.2 | SDK v1.0 release | agent-sdk-python | SDK Lead | Python SDK v1.0 (PyPI) |
| 10.3 | SDK v1.0 release | agent-sdk-typescript | SDK Lead | TypeScript SDK v1.0 (npm) |
| 10.4 | Formalize governance model | foundation | Governance | OpenTrade Foundation charter draft |
| 10.5 | Establish maintainer board | foundation | Admin | 3-5 core maintainers |
| 10.6 | Enterprise deployment guide | website | DevOps | Kubernetes, HA, multi-region |
| 10.7 | Compliance documentation | foundation | Legal | GDPR, PCI-DSS for escrow |
| 10.8 | Year-one retrospective | foundation | PM | Metrics, lessons, year-2 plan |

**Phase 4 Milestones:**
- [ ] Protocol v1.0 released
- [ ] Both SDKs v1.0 published
- [ ] Governance model established
- [ ] 25+ registered PEP nodes
- [ ] $100K+ transaction volume through escrow

---

### 4.5. Phase 5: Ecosystem Expansion (Months 13-18)

| # | Task | Priority | Status |
|------|--------|----------|--------|
| Federation v2 (gRPC streaming) | High | Planned |
| Multi-language SDKs (Rust, Java) | High | Planned |
| Mobile SDK (iOS/Android) | Medium | Planned |
| Dispute resolution automation | High | Planned |
| AI agent marketplace | Medium | Planned |
| L2 blockchain escrow (optional) | Low | Exploratory |
| OpenTrade Foundation incorporation | High | Planned |
| 50+ PEP nodes | High | Target |

---

### 4.6. Phase 6: Standardization (Months 19-24)

| # | Task | Priority | Status |
|------|--------|----------|--------|
| Industry standards body submission | High | Planned |
| 100+ PEP nodes | High | Target |
| 10+ category schemas | High | Target |
| Enterprise tier launch | Medium | Planned |
| Conference presence (OSS, AI, eCommerce) | Medium | Planned |
| 50+ active AI agent integrations | High | Target |

---

## 5. OPEN-SOURCE BEST PRACTICES

### 5.1. Licensing Strategy

| Component | License | Rationale |
|-----------|---------|-----------|
| **Protocol specs** (OpenAPI, JSON-LD, schemas) | **CC-BY 4.0** | Allows anyone to implement; attribution required; no patent grant needed for specs |
| **Protocol examples** | **CC0-1.0** | Public domain; encourages adoption without restrictions |
| **Reference implementations** (all code) | **Apache 2.0** | Permissive; allows commercial use; provides patent grant; preserves contributor copyright |
| **Documentation** | **CC-BY-SA 4.0** | Share-alike ensures improvements flow back |
| **Brand assets** (logo, name) | **All Rights Reserved** | Protects brand identity; prevents confusion |

#### License File Template for Code Repos

```apache
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.
      "License" shall mean the terms and conditions...

   [Full Apache 2.0 text]

   ADDITIONAL CLAUSE: Derivative Works
   Any derivative work of the Protocol specification must use a different
   name or clear branding to distinguish it from OpenTrade Protocol.
```

### 5.2. Protocol Change Process (RFC System)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Protocol Change Workflow                         │
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────────┐ │

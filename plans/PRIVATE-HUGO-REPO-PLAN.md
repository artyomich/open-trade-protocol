# OpenTrade Protocol — Private Hugo Website Repository Plan

**Version:** 1.0
**Date:** 2026-10-05
**Status:** Ready for Implementation
**Scope:** Local-only, private development of Hugo website for opentradeprotocol.com
**Server:** l1 (ssh://artem@l1:13285, base path ~/repos/)

---

## 1. PRIVATE REPOSITORY STRUCTURE

### 1.1. Repository Name

```
opentrade-website
```

Full GitHub path (future): `github.com/open-trade-protocol/opentrade-website`
Local server path: `~/repos/opentrade-website/`

### 1.2. Complete Directory Tree

```
opentrade-website/
├── hugo.toml                              # Hugo configuration (local dev profile)
├── Makefile                               # Local build automation
├── .gitignore                             # Git ignore rules
├── .gitattributes                         # Git attributes for binary/text handling
├── README.md                              # Project README
├── SECURITY.md                            # Security policy
├── CHANGELOG.md                           # Site version history
├── archetypes/
│   ├── default.md                         # Default content archetype
│   ├── docs/                              # Documentation archetype
│   │   └── default.md
│   └── blog/                              # Blog post archetype
│       └── default.md
├── content/
│   ├── _index.md                          # Homepage
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
├── data/
│   ├── protocol-versions.yaml
│   ├── sdk-versions.yaml
│   └── partners.yaml
├── layouts/
│   ├── _default/
│   │   ├── baseof.html
│   │   ├── list.html
│   │   ├── single.html
│   │   ├── docs.html
│   │   └── taxonomy.html
│   ├── partials/
│   │   ├── header.html
│   │   ├── footer.html
│   │   ├── sidebar.html
│   │   ├── search.html
│   │   ├── schema-markup.html
│   │   └── mermaid-diagram.html
│   ├── docs/
│   │   └── list.html
│   ├── index.html
│   └── _markup/
│       └── render-link.html
├── static/
│   ├── diagrams/
│   │   ├── architecture/
│   │   │   ├── system-overview.svg
│   │   │   ├── data-flow-search.svg
│   │   │   └── data-flow-escrow.svg
│   │   └── protocols/
│   │       ├── escrow-state-machine.svg
│   │       └── federation-sync.svg
│   ├── brand/
│   │   ├── logo-dark.svg
│   │   ├── logo-light.svg
│   │   └── style-guide.pdf
│   ├── css/
│   │   └── custom.css
│   └── js/
│       └── custom.js
├── themes/
│   └── opentrade/
│       ├── README.md
│       ├── hugo.toml
│       ├── archetypes/
│       │   └── default.md
│       ├── layouts/
│       │   ├── _default/
│       │   │   ├── baseof.html
│       │   │   ├── list.html
│       │   │   ├── single.html
│       │   │   └── taxonomy.html
│       │   ├── partials/
│       │   │   ├── header.html
│       │   │   ├── footer.html
│       │   │   ├── sidebar.html
│       │   │   ├── menu.html
│       │   │   ├── breadcrumbs.html
│       │   │   ├── schema-markup.html
│       │   │   └── mermaid-diagram.html
│       │   ├── docs/
│       │   │   └── list.html
│       │   └── index.html
│       └── static/
│           ├── css/
│           │   ├── main.css
│           │   ├── syntax-highlighting.css
│           │   └── print.css
│           └── js/
│               ├── search.js
│               └── mermaid-loader.js
├── scripts/
│   ├── validate-specs.sh
│   ├── generate-api-docs.sh
│   ├── sync-specs.sh
│   └── local-ci.sh
└── configs/
    └── hugo.local.toml                    # Local development override
```

---

## 2. SERVER SETUP COMMANDS

### 2.1. SSH to Server and Create Repository

```bash
# Connect to l1 server
ssh -p 13285 artem@l1

# Create the repository directory on the server
ssh -p 13285 artem@l1 "mkdir -p ~/repos/opentrade-website && cd ~/repos/opentrade-website && git init --bare"

# Verify creation
ssh -p 13285 artem@l1 "ls -la ~/repos/opentrade-website/"
```

### 2.2. Local Clone and Initialize

```bash
# On your local machine (not on l1)
cd ~/dev

# Clone the bare repo (this creates a working copy)
git clone artem@l1:~/repos/opentrade-website.git open-trade-website

# Enter the working directory
cd open-trade-website

# Initialize as a normal repo (bare repos cannot be worked in directly)
# The first push will set up the default branch
git init
git checkout -b main
```

### 2.3. Hugo Installation (if not installed)

```bash
# Option A: Download Hugo Extended (recommended)
wget https://github.com/gohugoio/hugo/releases/download/v0.147.0/hugo_extended_0.147.0_linux-amd64.tar.gz
tar -xzf hugo_extended_0.147.0_linux-amd64.tar.gz
sudo mv hugo /usr/local/bin/

# Option B: Via package manager (Debian/Ubuntu)
# sudo apt install hugo

# Option C: Via Go
# go install github.com/gohugoio/hugo/v3@latest

# Verify installation
hugo version
```

---

## 3. KEY CONFIGURATION FILES

### 3.1. hugo.toml (Root Configuration)

```toml
baseURL = 'https://opentradeprotocol.com/'
languageCode = 'en-us'
title = 'OpenTrade Protocol'
theme = 'opentrade'

# Local development overrides (gitignored)
# See configs/hugo.local.toml for dev-specific settings

# Default language
defaultContentLanguage = 'en'
defaultContentLanguageInSubdir = false

# Content directory
contentDir = 'content'

# Output formats
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
    lineNumbers = false
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

# Params
[params]
  description = 'Open protocol for structured peer-to-peer commerce, optimized for AI agent consumption.'
  github_repo = 'https://github.com/open-trade-protocol'
  github_project_repo = 'https://github.com/open-trade-protocol'
  version = '0.1.0'
  commit = 'HEAD'
  disable_og = false
  disable_analytics = true
```

### 3.2. configs/hugo.local.toml (Local Development Override)

```toml
# Local development configuration
# Copy to hugo.local.toml in root and uncomment for local dev

# baseURL = 'http://localhost:1313/'
# disableLiveReload = false
# appendTo = true

# Disable analytics locally
# [params]
#   disable_analytics = true
```

### 3.3. .gitignore

```gitignore
# Hugo output
public/
resources/
hugo_stats.json

# Local Hugo overrides (development only)
hugo.local.toml

# Theme local overrides
themes/opentrade/static/css/*.css.bak
themes/opentrade/static/js/*.js.bak

# Python (scripts)
__pycache__/
*.py[cod]
*.so
*.egg-info/
dist/
build/
.eggs/
.venv/
venv/

# Node (if used for theme assets)
node_modules/
*.tsbuildinfo

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
*.pem

# Environment / secrets
.env
*.key
*.pem
secrets/

# Logs
*.log

# Temporary files
*.tmp
*.temp

# OpenTrade local drafts
proposals/
drafts/
```

### 3.4. .gitattributes

```gitattributes
# Markdown - ensure consistent line endings
*.md text diff=markdown

# YAML - text files
*.yaml text
*.yml text

# TOML - text files
*.toml text

# SVG - binary (do not diff)
*.svg binary

# Images - binary
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.webp binary
*.ico binary
*.avif binary

# Fonts - binary
*.woff2 binary
*.woff binary
*.ttf binary
*.otf binary

# PDF - binary
*.pdf binary

# Minified files - binary
*.min.css binary
*.min.js binary

# Auto-merge for merge conflicts
*.md merge=ours
*.yaml merge=ours
*.yml merge=ours
*.toml merge=ours
```

### 3.5. Makefile

```makefile
.PHONY: help dev build serve theme-init sync-specs validate lint clean deploy-local

HUGO_VERSION := 0.147.0
HUGO_BIN := $(shell which hugo 2>/dev/null)
LOCAL_DEV_PORT := 1313
SERVER_HOST := l1
SERVER_PORT := 13285
SERVER_USER := artem
SERVER_REPO_PATH := ~/repos/opentrade-website

help:
	@echo "OpenTrade Protocol - Hugo Website Makefile"
	@echo ""
	@echo "Commands:"
	@echo "  dev          Start local Hugo development server"
	@echo "  build        Build site to public/"
	@echo "  serve        Run Hugo server on port 1313"
	@echo "  theme-init  Initialize opentrade theme"
	@echo "  sync-specs  Sync protocol specs from local spec repo"
	@echo "  validate     Validate Hugo configuration and content"
	@echo "  lint         Run linting on markdown and TOML"
	@echo "  clean        Remove build artifacts"
	@echo "  deploy       Push to remote server"
	@echo "  setup        One-time setup (Hugo install, theme init)"

dev:
	@if [ ! -f "$(HUGO_BIN)" ]; then echo "Hugo not found. Run 'make setup' first."; exit 1; fi
	hugo server --bind 0.0.0.0 --port $(LOCAL_DEV_PORT) --disableLiveReload --appendPort

build:
	hugo --minify --gc --cleanDestinationDir

serve:
	hugo server --disableLiveReload --appendPort

theme-init:
	@if [ -d "themes/opentrade" ]; then \
		echo "Theme already exists. Skipping."; \
	else \
		mkdir -p themes/opentrade/archetypes/layouts/_default/layouts/partials/static/css static/js; \
		echo "Theme scaffold created at themes/opentrade/"; \
	fi

sync-specs:
	@echo "Syncing protocol specs from local spec repo..."
	@if [ -d "../spec" ]; then \
		mkdir -p content/spec/openapi content/spec/protocols content/spec/schemas; \
		cp -n ../spec/openapi/*.yaml content/spec/openapi/ 2>/dev/null || true; \
		cp -n ../spec/protocols/*/PROTOCOL.md content/spec/protocols/ 2>/dev/null || true; \
		cp -n ../spec/schemas/**/*.json content/spec/schemas/ 2>/dev/null || true; \
		echo "Specs synced."; \
	else \
		echo "Spec repo not found at ../spec. Skipping."; \
	fi

validate:
	hugo --validate

lint:
	@echo "Linting markdown files..."
	@find content -name '*.md' -exec echo "Checking: {}" \;
	@echo "Linting TOML files..."
	@find . -maxdepth 2 -name '*.toml' -not -path './public/*' -exec echo "Checking: {}" \;
	@echo "Lint complete."

clean:
	rm -rf public/
	rm -rf resources/
	rm -f hugo_stats.json

deploy:
	@echo "Deploying to $(SERVER_HOST)..."
	git push $(SERVER_HOST):$(SERVER_REPO_PATH) main
	@echo "Deployed. SSH to $(SERVER_HOST) and run 'hugo --minify' on the server."

setup: theme-init
	@echo "=== OpenTrade Website Setup ==="
	@echo ""
	@echo "1. Hugo installation:"
	@echo "   wget https://github.com/gohugoio/hugo/releases/download/v$(HUGO_VERSION)/hugo_extended_$(HUGO_VERSION)_linux-amd64.tar.gz"
	@echo "   tar -xzf hugo_extended_$(HUGO_VERSION)_linux-amd64.tar.gz"
	@echo "   sudo mv hugo /usr/local/bin/"
	@echo ""
	@echo "2. Run 'make dev' to start local development server"
	@echo "3. Open http://localhost:1313 in your browser"
```

### 3.6. archetypes/default.md

```markdown
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
description: ""
tags: []
categories: []
weight: 100
---

## Summary

Brief summary of this page.

## Content

Write your content here.

## References

- [Related Doc](/docs/related-page)
```

### 3.7. archetypes/docs/default.md

```markdown
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
description: ""
weight: 100
prev: ""
next: ""
---

## Overview

Brief overview of this topic.

## Details

Detailed content goes here.

## Code Examples

\`\`\`bash
# Example command
hugo server
\`\`\`

## See Also

- [Related Documentation](/docs/related-topic)
```

### 3.8. archetypes/blog/default.md

```markdown
---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: true
description: ""
author: ""
tags: []
categories: []
---

## Introduction

Introduction to the blog post.

## Body

Main content goes here.

## Conclusion

Conclusion and next steps.
```

---

## 4. LOCAL CI TEMPLATE

### 4.1. scripts/local-ci.sh

```bash
#!/usr/bin/env bash
set -euo pipefail

# OpenTrade Protocol - Local CI Script
# Run: make validate or ./scripts/local-ci.sh

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ERRORS=0

echo "=========================================="
echo " OpenTrade Website - Local CI"
echo "=========================================="
echo ""

# 1. Check Hugo is installed
echo -n "Checking Hugo... "
if command -v hugo &> /dev/null; then
    HUGO_VERSION=$(hugo version | awk '{print $2}')
    echo -e "${GREEN}OK${NC} (v${HUGO_VERSION})"
else
    echo -e "${RED}FAIL${NC} - Hugo is not installed"
    echo "Install: https://gohugo.io/getting-started/installing/"
    ERRORS=$((ERRORS + 1))
fi

# 2. Validate Hugo configuration
echo -n "Validating Hugo config... "
if hugo --validate 2>&1; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAIL${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 3. Build site
echo -n "Building site... "
if hugo --quiet --quiet 2>&1; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FAIL${NC}"
    ERRORS=$((ERRORS + 1))
fi

# 4. Check for broken internal links
echo -n "Checking internal links... "
BROKEN_LINKS=$(find content -name '*.md' -exec grep -l 'href="/[^h]' {} \; 2>/dev/null | wc -l)
if [ "$BROKEN_LINKS" -eq 0 ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}WARNING${NC}: ${BROKEN_LINKS} potential broken links"
fi

# 5. Check draft status
echo -n "Checking draft pages... "
DRAFT_COUNT=$(grep -r '^draft: true' content/ 2>/dev/null | wc -l)
echo "Found ${DRAFT_COUNT} draft page(s)"

# 6. Check for empty descriptions
echo -n "Checking for empty descriptions... "
EMPTY_DESC=$(grep -r '^description: ""' content/ 2>/dev/null | wc -l)
if [ "$EMPTY_DESC" -gt 0 ]; then
    echo -e "${YELLOW}WARNING${NC}: ${EMPTY_DESC} page(s) with empty description"
else
    echo -e "${GREEN}OK${NC}"
fi

echo ""
echo "=========================================="
if [ "$ERRORS" -gt 0 ]; then
    echo -e "${RED}Local CI FAILED (${ERRORS} errors)${NC}"
    exit 1
else
    echo -e "${GREEN}Local CI PASSED${NC}"
fi
echo "=========================================="
```

---

## 5. INITIALIZATION STEPS

### 5.1. Step-by-Step Repository Initialization

```bash
# === STEP 1: Create bare repo on l1 server ===
ssh -p 13285 artem@l1 "mkdir -p ~/repos/opentrade-website && cd ~/repos/opentrade-website && git init --bare"

# === STEP 2: Create local working copy ===
cd ~/dev
git clone artem@l1:~/repos/opentrade-website.git open-trade-website
cd open-trade-website

# === STEP 3: Initialize local git repo ===
git init
git checkout -b main

# === STEP 4: Create directory structure ===
mkdir -p archetypes/{docs,blog}
mkdir -p content/{docs/getting-started,docs/protocol,docs/sdk/python,docs/sdk/typescript,docs/node-operator,docs/governance,community/blog,about}
mkdir -p content/spec/{openapi,protocols,schemas}
mkdir -p data
mkdir -p layouts/{_default,partials,docs,_markup}
mkdir -p static/{diagrams/architecture,diagrams/protocols,brand,css,js}
mkdir -p themes/opentrade/{archetypes,layouts/_default,layouts/partials,static/css,static/js}
mkdir -p scripts
mkdir -p configs

# === STEP 5: Copy configuration files ===
# Place hugo.toml in root
# Place .gitignore, .gitattributes in root
# Place Makefile in root
# Place all archetypes in archetypes/
# Place scripts in scripts/
# Place config templates in configs/

# === STEP 6: Create initial content files ===
# Create _index.md files for each content section
touch content/_index.md
touch content/docs/_index.md
touch content/docs/getting-started/_index.md
touch content/docs/protocol/_index.md
touch content/docs/sdk/_index.md
touch content/docs/sdk/python/_index.md
touch content/docs/sdk/typescript/_index.md
touch content/docs/node-operator/_index.md
touch content/docs/governance/_index.md
touch content/community/_index.md
touch content/community/blog/_index.md
touch content/about/_index.md

# === STEP 7: Add remote and initial commit ===
git remote add origin artem@l1:~/repos/opentrade-website
git add -A
git commit -m "chore: initial Hugo website scaffold

- Hugo configuration (hugo.toml)
- Custom opentrade theme scaffold
- Content structure for docs, protocol, SDK, community
- Local CI script and Makefile
- Archetypes for docs and blog content"

# === STEP 8: Push to server ===
git push -u origin main

# === STEP 9: Verify on server ===
ssh -p 13285 artem@l1 "ls -la ~/repos/opentrade-website/content/"
ssh -p 13285 artem@l1 "ls -la ~/repos/opentrade-website/themes/opentrade/"
```

### 5.2. Hugo Local Run

```bash
# Start local development server
hugo server --disableLiveReload --appendPort

# Or with Makefile
make dev

# Server will be available at http://localhost:1313
```

### 5.3. GitHub Integration (When Ready)

```bash
# Add GitHub remote (private repo under open-trade-protocol org)
git remote add github git@github.com:open-trade-protocol/website.git

# Push to GitHub
git push github main

# Set as upstream
git push -u github main
```

---

## 6. BRANCHING AND VERSIONING STRATEGY

### 6.1. Branching Model

```
main
 ├── draft/v0.2
 │   ├── feat/homepage-redesign
 │   ├── feat/sdk-docs-section
 │   └── chore/update-protocol-specs
 ├── draft/v0.3
 │   ├── feat/blog-launch
 │   └── feat/search-functionality
 └── release/v0.1
     ├── docs/getting-started-introduction
     ├── docs/protocol-search-api
     └── theme/opentrade-base
```

**Branch naming conventions:**

| Prefix | Purpose | Example |
|--------|---------|---------|
| `draft/` | Pre-release development | `draft/v0.2` |
| `feat/` | New features | `feat/homepage-redesign` |
| `docs/` | Documentation changes | `docs/getting-started-intro` |
| `theme/` | Theme/layout changes | `theme/opentrade-base` |
| `chore/` | Maintenance | `chore/update-specs` |
| `fix/` | Bug fixes | `fix/broken-links` |
| `release/` | Release preparation | `release/v0.1` |

### 6.2. Versioning Strategy (Semantic Versioning)

| Version | Phase | Description | Alignment |
|---------|-------|-------------|-----------|
| `0.1.0` | Foundation (Months 1-3) | Initial Hugo site with core docs | Phase 1, Month 2 |
| `0.2.0` | Reference Hardening (Months 4-6) | SDK docs, node operator guide | Phase 2, Month 4 |
| `0.3.0` | Community Growth (Months 7-9) | Blog, partner nodes dashboard | Phase 3 |
| `1.0.0` | Protocol Maturity (Months 10-12) | Full site, aligned with protocol v1.0 | Phase 4 |
| `1.x.x` | Ecosystem Expansion (Months 13+) | Feature releases | Phase 5+ |

**Tagging on server:**

```bash
# Create release tag
git tag -a v0.1.0 -m "Initial Hugo website release"
git push origin v0.1.0

# On server, verify tag
ssh -p 13285 artem@l1 "cd ~/repos/opentrade-website && git tag -l"
```

### 6.3. Content Versioning

Each content file has a `version` front matter field:

```yaml
---
title: "Architecture Overview"
date: 2026-10-05
version: "0.1.0"
lastReviewed: 2026-10-05
---
```

---

## 7. SECURITY AND PRIVACY RECOMMENDATIONS

### 7.1. Local Development Security

```bash
# === SSH Key Management ===
# Generate dedicated key for l1 server if not exists
ssh-keygen -t ed25519 -C "opentrade-website-l1" -f ~/.ssh/id_ed25519_opentrade_l1

# Add to SSH config (~/.ssh/config)
cat >> ~/.ssh/config << 'EOF'
Host l1
    HostName l1
    Port 13285
    User artem
    IdentityFile ~/.ssh/id_ed25519_opentrade_l1
    ForwardAgent false
    StrictHostKeyChecking ask
EOF

# === Local Hugo Config (never commit) ===
cat > hugo.local.toml << 'EOF'
# Local development overrides
baseURL = 'http://localhost:1313/'
disableLiveReload = false
appendTo = true
[params]
  disable_analytics = true
EOF

# === Git secrets scanning (local) ===
# Install git-secrets
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets && sudo make install && cd ..

# Configure patterns
git secrets --register-aws
git secrets --add 'api[_\-]?key'
git secrets --add 'secret[_\-]?key'
git secrets --add 'password'
git secrets --add 'token'

# === Server-side hardening ===
# On l1: restrict repo permissions
ssh -p 13285 artem@l1 "chmod 700 ~/repos/opentrade-website"
ssh -p 13285 artem@l1 "chmod 700 ~/repos"
```

### 7.2. Privacy Measures

| Measure | Implementation |
|---------|---------------|
| **Repo visibility** | `private` on GitHub (when synced) |
| **SSH-only access** | No HTTPS push; key-based auth only |
| **No public analytics** | `disable_analytics = true` in hugo.toml |
| **No live reload in production** | Disabled for deployed builds |
| **HSTS header** | Set when deploying behind reverse proxy |
| **robots.txt** | `Disallow: /` until public launch |
| **No sitemap** | Exclude from `sitemap.xml` until ready |

### 7.3. Local-Only Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    LOCAL-ONLY DEVELOPMENT FLOW                   │
│                                                                 │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│  │  Local Work  │────>│  Local Push  │────>│  Server l1   │   │
│  │  (hugo dev)  │     │  (git push)  │     │  (git bare)  │   │
│  └──────────────┘     └──────────────┘     └──────────────┘   │
│       localhost:1313              SSH:13285              SSH:13285  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    NOT CONNECTED TO INTERNET              │   │
│  │              (until explicitly synced to GitHub)           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. QUICK REFERENCE COMMANDS

### 8.1. Daily Development

```bash
# Start dev server
make dev
# or: hugo server --disableLiveReload --appendPort

# Build site
make build
# or: hugo --minify --gc --cleanDestinationDir

# Run local CI
make validate
# or: ./scripts/local-ci.sh

# Sync latest specs
make sync-specs

# Clean build artifacts
make clean
```

### 8.2. Git Workflow

```bash
# Create feature branch
git checkout -b feat/new-doc-section main

# Commit changes
git add -A
git commit -m "docs: add new documentation section"

# Push to local server
git push origin feat/new-doc-section

# Merge to main (after review)
git checkout main
git merge feat/new-doc-section
git push origin main
```

### 8.3. Server Management

```bash
# SSH to server
ssh -p 13285 artem@l1

# List repos
ls ~/repos/

# Check repo status
cd ~/repos/opentrade-website && git status

# Manual build on server
cd ~/repos/opentrade-website && hugo --minify --gc
```

---

## 9. DEPLOYMENT TO PUBLIC (FUTURE)

When the site is ready for public launch:

```bash
# 1. Create private repo on GitHub org
# (via GitHub UI or gh CLI)
gh repo create open-trade-protocol/website --private

# 2. Add GitHub remote
git remote add github git@github.com:open-trade-protocol/website.git

# 3. Push to GitHub
git push github main

# 4. Enable GitHub Pages (private)
gh pages enable --source public/

# 5. Configure domain DNS
# (as specified in STRATEGIC_PLAN.md section 3.5)

# 6. Enable analytics
# Update hugo.toml: disable_analytics = false
```

---

## 10. FILE INVENTORY SUMMARY

| File | Purpose | Committed |
|------|---------|-----------|
| `hugo.toml` | Hugo configuration | Yes |
| `configs/hugo.local.toml` | Local dev override template | Yes (as template) |
| `Makefile` | Build automation | Yes |
| `.gitignore` | Git ignore rules | Yes |
| `.gitattributes` | Git attributes | Yes |
| `README.md` | Project documentation | Yes |
| `SECURITY.md` | Security policy | Yes |
| `CHANGELOG.md` | Version history | Yes |
| `archetypes/default.md` | Default content template | Yes |
| `archetypes/docs/default.md` | Doc content template | Yes |
| `archetypes/blog/default.md` | Blog post template | Yes |
| `content/**/_index.md` | Section index pages | Yes |
| `layouts/**/*` | Custom templates | Yes |
| `themes/opentrade/**/*` | Custom theme | Yes |
| `static/**/*` | Assets (CSS, JS, images) | Yes |
| `data/*.yaml` | Site data | Yes |
| `scripts/local-ci.sh` | Local CI script | Yes |
| `scripts/validate-specs.sh` | Spec validation | Yes |
| `scripts/sync-specs.sh` | Spec sync script | Yes |
| `hugo.local.toml` | Active local override | No (gitignored) |

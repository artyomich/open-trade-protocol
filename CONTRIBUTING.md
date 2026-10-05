# Contributing to OpenTrade Protocol

Thank you for your interest in contributing to OpenTrade Protocol. This document outlines the process and guidelines for contributing.

## How to Contribute

### 1. Protocol Specifications

We welcome contributions to the protocol specifications:

- **Category schemas** — Add new product categories in `spec/schemas/categories/`
- **Protocol extensions** — Propose new protocol features in `spec/protocols/`
- **Examples** — Add realistic data samples in `spec/examples/`

### 2. Agent SDKs

- Python SDK: `reference-impl/agent-sdk/python/`
- TypeScript SDK: `reference-impl/agent-sdk/typescript/`

Submit PRs with new features, bug fixes, or documentation improvements.

### 3. Node Implementations

We welcome reference implementations for different languages and frameworks.

## Contribution Process

1. Fork the repository
2. Create a feature branch (`feature/add-shoes-category`)
3. Make your changes
4. Submit a pull request with a clear description

## Protocol Change Process

Major protocol changes follow a formal process:

1. **Proposal** — Create `proposals/YYYY-MM-DD-description.md`
2. **Discussion** — Open an issue for community feedback
3. **Implementation** — Reference implementation in the proposal PR
4. **Review** — Core maintainers review for correctness and compatibility
5. **Adoption** — Merge into `main` as a draft protocol version
6. **Stabilization** — Monitor usage, collect feedback
7. **Release** — Promote to stable when widely adopted

## Coding Standards

### Python
- Type hints on all public functions
- Docstrings following Google style
- No external dependencies (stdlib only)

### TypeScript
- Strict mode enabled
- JSDoc on all exported types and functions
- No `any` types

### Protocol Specs
- YAML for OpenAPI spec (validated)
- JSON for examples (validated)
- Markdown for protocol docs
- All URLs use `https://`

## Review Process

All PRs require:
- At least one maintainer approval
- CI pass (spec validation, linting)
- Clear description of changes
- Updated documentation if applicable

## Getting Help

- **Protocol questions** — Open an issue with label `question`
- **Bug reports** — Open an issue with label `bug`
- **Feature requests** — Open an issue with label `enhancement`
- **Quick chat** — Discord/Telegram (link to be added)

## Code of Conduct

Be respectful, inclusive, and constructive. Harassment of any kind will not be tolerated.

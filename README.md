# Atlas v2

Atlas v2 is an AI agent runtime built with Python 3.13. It provides a modular foundation for building production-grade AI agents with pluggable LLM providers, tool registries, memory backends, and a contract-tested architecture.

## Features

- **Runtime** — Agent execution engine
- **Providers** — Pluggable LLM provider adapters
- **Tools** — Tool definitions and registry
- **Memory** — Pluggable memory backends
- **Models** — Data models and schemas
- **Config** — Configuration management
- **Prompts** — Prompt templates
- **Utils** — Shared utilities

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (package manager)

## Installation

```bash
uv sync
```

This creates a virtual environment (`.venv`) and installs all runtime and development dependencies from `uv.lock`.

## Usage

Run the CLI entry point:

```bash
uv run atlas
```

Outputs:

```
Atlas v2 (version 0.1.0)
```

## Project Structure

```
Atlas-v2/
├── docs/                  # Documentation
├── src/
│   └── atlas/
│       ├── runtime/       # Agent execution engine
│       ├── providers/     # LLM provider adapters
│       ├── tools/         # Tool definitions and registry
│       ├── memory/        # Memory backends
│       ├── models/        # Data models and schemas
│       ├── config/        # Configuration management
│       ├── prompts/       # Prompt templates
│       └── utils/         # Shared utilities
├── tests/
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── contract/          # Contract tests
├── pyproject.toml
├── uv.lock
└── README.md
```

## Testing

Run the full test suite:

```bash
uv run pytest
```

Run a specific test group:

```bash
uv run pytest -m "unit"          # unit tests only
uv run pytest -m "integration"   # integration tests only
uv run pytest -m "contract"      # contract tests only
```

## Linting & Formatting

The project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
uv run ruff check .        # lint
uv run ruff format .       # format
uv run ruff check --fix .  # lint + auto-fix
```

## Type Checking

The project uses [mypy](https://mypy-lang.org/) with strict mode:

```bash
uv run mypy
```

## Development

Install the development dependencies:

```bash
uv sync --dev
```

## License

This project is currently unlicensed — no license has been specified yet.

## Author

- **rahomi** — [mohib.hossain.bu@gmail.com](mailto:mohib.hossain.bu@gmail.com)
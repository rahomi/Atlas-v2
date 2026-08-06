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
- **Logging** — Structured logging via `structlog`

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

## Logging

Atlas v2 uses [structlog](https://www.structlog.org/) for structured, key-value logging.

### Configure logging at startup

```python
from atlas.config import configure_logging

configure_logging()
```

### Get a named logger

```python
from atlas.utils import get_logger

logger = get_logger("my_component")

logger.info("event_occurred", key="value", count=42)
```

### Use the module-level default logger

```python
from atlas.utils.logger import logger

logger.warning("api_key_missing")
```

### Logging settings

The following environment variables control logging behavior (defined in `atlas.config.Settings`):

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Minimum log level to emit |
| `LOG_JSON` | `false` | Emit logs as JSON instead of pretty-printed console output |

Set them in your `.env` file or environment:

```bash
LOG_LEVEL=DEBUG
LOG_JSON=true
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
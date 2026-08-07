# Atlas v2

Atlas v2 is an AI agent runtime built with Python 3.13. It provides a modular foundation for building production-grade AI agents with pluggable LLM providers, tool registries, memory backends, and a contract-tested architecture.

## Features

- **Runtime** — Agent execution engine with tool-call loops and configurable iteration limits
- **Providers** — Pluggable LLM provider adapters (Ollama, fake/test providers)
- **Tools** — Tool definitions, schema validation, and a registry with a built-in calculator tool
- **Memory** — Pluggable memory backend interface (extensible via contract)
- **Models** — Pydantic data models for messages, conversations, roles, and tool calls
- **Config** — Environment-based configuration via `pydantic-settings`
- **Prompts** — Prompt template namespace
- **Utils** — Shared utilities
- **Logging** — Structured logging via `structlog`
- **Contract Testing** — Architecture contract tests plus unit and integration test suites

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (package manager)

## Installation

```bash
uv sync
```

This creates a virtual environment (`.venv`) and installs all runtime and development dependencies from `uv.lock`.

## Configuration

Atlas reads configuration from environment variables or a `.env` file (see `.env.example`). The settings are defined in `atlas.config.Settings`.

| Variable | Default | Description |
|----------|---------|-------------|
| `ATLAS_PROVIDER` | `ollama` | Active LLM provider (`ollama`, `fake`) |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama API endpoint |
| `OLLAMA_MODEL` | `qwen3:latest` | Default Ollama model |
| `OPENAI_API_KEY` | *(empty)* | OpenAI API key (for OpenAI-backed providers) |
| `OPENAI_MODEL` | `gpt-5` | Default OpenAI model |
| `LOG_LEVEL` | `INFO` | Minimum log level to emit |
| `LOG_JSON` | `false` | Emit logs as JSON instead of pretty-printed console output |

Example `.env`:

```bash
ATLAS_PROVIDER=ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=qwen3:latest
LOG_LEVEL=DEBUG
LOG_JSON=true
```

## Quick Start

Run the CLI entry point:

```bash
uv run atlas
```

Outputs:

```
Atlas v2 (version 0.1.0)
```

### Use the agent runtime

```python
import asyncio

from atlas.config import configure_logging
from atlas.models import Conversation, Message, MessageRole
from atlas.providers.tool_fake import FakeToolCallingModel
from atlas.runtime.agent import AgentRuntime
from atlas.tools.calculator import CalculatorTool
from atlas.tools.registry import ToolRegistry


async def main() -> None:
    configure_logging()

    tools = ToolRegistry()
    tools.register(CalculatorTool())

    model = FakeToolCallingModel()
    agent = AgentRuntime(model=model, tools=tools, max_iterations=10)

    conversation = Conversation(
        messages=(
            Message(role=MessageRole.USER, content="What is 25 * 48?"),
        )
    )

    response = await agent.run(conversation)
    print(response.content)


asyncio.run(main())
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

## Project Structure

```
Atlas-v2/
├── docs/                  # Documentation
├── src/
│   └── atlas/
│       ├── runtime/       # Agent execution engine
│       │   ├── agent.py            # Agent loop
│       │   ├── contracts.py        # ModelClient / Tool / Memory contracts
│       │   ├── model_response.py   # Model response model
│       │   ├── result.py           # Generic Result wrapper
│       │   └── tool_result.py      # Tool result model
│       ├── providers/     # LLM provider adapters
│       │   ├── ollama.py       # Ollama provider
│       │   ├── fake.py         # Deterministic fake provider (tests/demos)
│       │   └── tool_fake.py    # Fake provider with tool support
│       ├── tools/         # Tool definitions and registry
│       │   ├── calculator.py    # Built-in calculator tool
│       │   ├── registry.py      # Tool registry
│       │   └── schemas.py       # Tool argument schemas
│       ├── memory/        # Memory backend interface
│       ├── models/        # Data models and schemas
│       │   ├── message.py       # Message model
│       │   ├── conversation.py  # Conversation model
│       │   ├── roles.py         # Message role enum
│       │   └── tool_call.py     # Tool-call model
│       ├── config/        # Configuration management
│       │   ├── settings.py      # pydantic-settings Settings
│       │   └── logging.py       # structlog configuration
│       ├── prompts/       # Prompt templates
│       └── utils/         # Shared utilities (logger)
├── tests/
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests (agent behavior)
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
~~~

A few things I verified against the codebase while writing it:

- The runtime class is `AgentRuntime` (exported from `atlas.runtime`), and its constructor takes `model`, `tools`, and `max_iterations`.
- The agent loop is **async** — so the example uses `asyncio.run(...)`.
- The fake tool-calling provider is `FakeToolCallingModel` (from `atlas.providers.tool_fake`), and the fake echo provider is `FakeModelClient` (from `atlas.providers.fake`).
- The env var names (`ATLAS_PROVIDER`, `OLLAMA_HOST`, etc.) match `atlas.config.Settings`.
- Test markers (`unit`, `integration`, `contract`) match the `pyproject.toml` pytest configuration.

One caveat: `configure_logging()` currently hardcodes `INFO` and doesn't yet read `LOG_LEVEL`/`LOG_JSON` from `Settings` — the settings are defined and parsed, but the wiring isn't done yet. I documented the env vars as "defined in Settings" without claiming `configure_logging` honors them yet, so the README stays accurate until that's implemented.
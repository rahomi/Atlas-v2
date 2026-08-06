from atlas.config.logging import configure_logging
from atlas.utils.logger import logger

configure_logging()

logger.info(
    "application_started",
    version="0.1.0",
)

logger.info(
    "provider_selected",
    provider="ollama",
)

logger.warning(
    "api_key_missing",
)
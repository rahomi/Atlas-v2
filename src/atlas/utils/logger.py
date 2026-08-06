import structlog


def get_logger(name: str | None = None) -> structlog.stdlib.BoundLogger:
    """Get a bound structlog logger.

    Args:
        name: Optional logger/component name.

    Returns:
        A bound logger.
    """
    return structlog.get_logger(name) if name else structlog.get_logger()


logger = structlog.get_logger()


__all__ = ["get_logger", "logger"]
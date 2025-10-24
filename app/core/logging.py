import logging
import sys
from typing import Optional


def setup_logging(level: str = "INFO", uvicorn_override: bool = True) -> None:
    """Configure root logging and optionally align uvicorn loggers.

    Parameters
    ----------
    level: str
        Logging level name, e.g., "DEBUG", "INFO".
    uvicorn_override: bool
        When True, propagate uvicorn loggers to root to unify formatting.
    """
    log_level = getattr(logging, level.upper(), logging.INFO)

    # Basic config
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    if uvicorn_override:
        for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
            logger = logging.getLogger(logger_name)
            logger.handlers.clear()
            logger.propagate = True

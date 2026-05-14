"""
Logging configuration helpers for the Route Explorer app.
"""

import logging
from pathlib import Path


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Configure console and file logging for the application.

    Args:
        log_level: Logging level name such as INFO or DEBUG.

    Returns:
        Configured root logger.
    """
    level = getattr(logging, log_level.upper(), logging.INFO)
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(level)

    if logger.handlers:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(logs_dir / "route_explorer.log", encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.debug("Logging initialized at level %s", logging.getLevelName(level))
    return logger
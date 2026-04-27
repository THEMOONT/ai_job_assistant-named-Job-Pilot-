import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger(name: str, filename: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler — rotates at 5MB, keeps 3 backups
    file_handler = RotatingFileHandler(
        os.path.join(LOG_DIR, filename),
        maxBytes=5 * 1024 * 1024,
        backupCount=3
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


# Pre-built loggers for each module
auth_logger    = setup_logger("auth",    "auth.log")
actions_logger = setup_logger("actions", "actions.log")
apply_logger   = setup_logger("apply",   "apply.log")
api_logger     = setup_logger("api",     "api.log")
error_logger   = setup_logger("errors",  "errors.log", level=logging.ERROR)

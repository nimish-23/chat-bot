import logging
import sys
from logging.handlers import RotatingFileHandler
import os


def setup_logger():
    logger = logging.getLogger("chatbot")
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)

    # File Handler (Rotating)
    file_handler = RotatingFileHandler(
        "logs/chatbot.log",
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


logger = setup_logger()

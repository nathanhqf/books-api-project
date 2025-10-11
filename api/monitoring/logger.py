"""
Sistema de Logs Estruturados
"""

import logging
import sys
from pythonjsonlogger import jsonlogger
from pathlib import Path

def setup_logger(name: str = "books_api") -> logging.Logger:
    """Configura logger com formato JSON"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para arquivo
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / "api.log")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

api_logger = setup_logger()

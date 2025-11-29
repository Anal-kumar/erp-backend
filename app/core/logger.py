"""
Structured logging configuration for production-grade application
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
import json
from datetime import datetime
from typing import Any, Dict

# Create logs directory if it doesn't exist
LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(exist_ok=True)

class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging
    """
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        return json.dumps(log_data)


def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Setup logger with file and console handlers
    
    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Console handler with simple format for development
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # File handler with JSON format for production
    file_handler = RotatingFileHandler(
        LOGS_DIR / f"{name}.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(JSONFormatter())
    logger.addHandler(file_handler)
    
    # Error file handler
    error_handler = RotatingFileHandler(
        LOGS_DIR / f"{name}_error.log",
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    logger.addHandler(error_handler)
    
    return logger


# Create application logger
app_logger = setup_logger("rice_mill_erp", level="INFO")


def log_request(method: str, url: str, status_code: int, duration: float, **kwargs):
    """Log HTTP request"""
    app_logger.info(
        f"{method} {url} - {status_code}",
        extra={
            "method": method,
            "url": url,
            "status_code": status_code,
            "duration_ms": round(duration * 1000, 2),
            **kwargs
        }
    )


def log_error(message: str, error: Exception = None, **kwargs):
    """Log error with context"""
    app_logger.error(
        message,
        exc_info=error,
        extra=kwargs
    )


def log_security_event(event_type: str, details: Dict[str, Any]):
    """Log security-related events"""
    app_logger.warning(
        f"Security Event: {event_type}",
        extra={
            "event_type": event_type,
            "security": True,
            **details
        }
    )

import logging
import sys
import traceback
from logging import Formatter, StreamHandler
from typing import Dict, Any
from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.logger import logger as fastapi_logger
import re


class ColoredFormatter(Formatter):
    """Custom formatter to add color codes to log levels."""
    COLORS = {
        logging.DEBUG: "\033[94m",     # Blue
        logging.INFO: "\033[92m",      # Green
        logging.WARNING: "\033[93m",   # Yellow
        logging.ERROR: "\033[91m",     # Red
        logging.CRITICAL: "\033[95m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record):
        level_color = self.COLORS.get(record.levelno, self.RESET)
        message = super().format(record)
        return f"{level_color}{message}{self.RESET}"


class CustomLogger:
    def __init__(self, name: str = "fastapi", log_level: int = logging.DEBUG,
                 log_headers: bool = False):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        console_handler = StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)

        formatter = ColoredFormatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        console_handler.setFormatter(formatter)

        self.logger.addHandler(console_handler)
        fastapi_logger.handlers = self.logger.handlers
        fastapi_logger.setLevel(self.logger.level)

        self.log_headers = log_headers

        # Define sensitive patterns
        self.SENSITIVE_PATTERNS = [
            # Authorization headers/tokens
            r"(?:authorization|auth-token|token)[:=\s]*[^\s]+",
            # Long numbers (credit cards, IDs)
            r"[0-9]{13,19}",
            # Email addresses
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}",
            # Credit card numbers without dashes
            r"\d{16}",
            r"\d{3}-\d{2}-\d{4}"                               # SSN format
        ]
        self.SENSITIVE_KEYS = (
            "headers",
            "credentials",
            "Authorization",
            "token",
            "password",
        )

    def _sanitize_message(self, message: str) -> str:
        """Sanitize sensitive data from log messages."""
        sanitized = message
        for pattern in self.SENSITIVE_PATTERNS:
            sanitized = re.sub(
                pattern, "[REDACTED]", sanitized, flags=re.IGNORECASE)
        return sanitized

    def _sanitize_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize sensitive data in dictionaries."""
        if not isinstance(data, dict):
            return data

        sanitized = {}
        for key, value in data.items():
            if key.lower() in self.SENSITIVE_KEYS:
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_dict(value)
            elif isinstance(value, str):
                sanitized[key] = self._sanitize_message(value)
            else:
                sanitized[key] = value
        return sanitized

    def log_request(self, request: Request):
        """Log details of the incoming request."""
        self.logger.info("Incoming request: %s %s",
                         request.method, request.url)

        if self.log_headers:
            sanitized_headers = self._sanitize_dict(dict(request.headers))
            self.logger.debug("Headers: %r", sanitized_headers)

        self.logger.debug("Query params: %r",
                          self._sanitize_dict(dict(request.query_params)))

        if hasattr(request, "json"):
            try:
                body = request.json()
                sanitized_body = self._sanitize_dict(body)
                self.logger.debug("Body: %r", sanitized_body)
            except Exception:
                self.logger.debug("Failed to parse request body")

    def log_response(self, response: Response):
        """Log details of the outgoing response."""
        self.logger.info("Outgoing response: Status %s",
                         response.status_code)

        if self.log_headers:
            sanitized_headers = self._sanitize_dict(dict(response.headers))
            self.logger.debug("Headers: %r", sanitized_headers)

        if hasattr(response, "body"):
            try:
                body = response.body.decode()
                sanitized_body = self._sanitize_message(body)
                self.logger.debug("Body: %r", sanitized_body)
            except Exception:
                self.logger.debug("Failed to parse response body")

    def log_exception(self, exc: Exception):
        """Log exceptions with traceback."""
        self.logger.error("Exception occurred: %s", str(exc))
        self.logger.error("%s", traceback.format_exc())

    def debug(self, message: str, extra: Dict[str, Any] = None):
        sanitized_message = self._sanitize_message(message)
        self.logger.debug("%s", sanitized_message, extra=extra)

    def info(self, message: str, extra: Dict[str, Any] = None):
        sanitized_message = self._sanitize_message(message)
        self.logger.info("%s", sanitized_message, extra=extra)

    def warning(self, message: str, extra: Dict[str, Any] = None):
        sanitized_message = self._sanitize_message(message)
        self.logger.warning("%s", sanitized_message, extra=extra)

    def error(self, message: str, extra: Dict[str, Any] = None):
        sanitized_message = self._sanitize_message(message)
        self.logger.error("%s", sanitized_message, extra=extra)

    def critical(self, message: str, extra: Dict[str, Any] = None):
        sanitized_message = self._sanitize_message(message)
        self.logger.critical("%s", sanitized_message, extra=extra)

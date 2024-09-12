import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response
import time


class DetailedLogger:
    def __init__(self, name: str, log_file: str = "app.log", log_level: int = logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]'
        )

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        log_dir = Path(__file__).parents[2] / 'logs'
        log_dir.mkdir(exist_ok=True)
        file_handler = RotatingFileHandler(
            log_dir / log_file, maxBytes=10*1024*1024, backupCount=5
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message, exc_info=True)

    def critical(self, message: str):
        self.logger.critical(message, exc_info=True)


class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.logger = DetailedLogger("fastapi_app")

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        self.logger.info(f"{request.method} {
                         request.url.path} - Status: {response.status_code} - Duration: {process_time:.4f}s")
        return response


logger = DetailedLogger("fastapi_app")


def get_logger():
    return logger

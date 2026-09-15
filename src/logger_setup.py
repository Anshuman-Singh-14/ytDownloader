
import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logger():
    logger = logging.getLogger("YTDownloader")
    if not logger.handlers: # Prevent duplicate logs if called twice
        logger.setLevel(logging.DEBUG)
        log_format = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(threadName)-15s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler = RotatingFileHandler('downloader.log', maxBytes=5*1024*1024, backupCount=3)
        file_handler.setFormatter(log_format)
        file_handler.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        console_handler.setLevel(logging.INFO)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

class YTDLPLogger:
    """Redirects yt-dlp's internal console printouts into our Python logger."""
    def __init__(self, logger):
        self.logger = logger

    def debug(self, msg):
        if msg.startswith('[debug]'):
            self.logger.debug(f"yt-dlp: {msg}")
        else:
            self.logger.info(f"yt-dlp: {msg}")

    def info(self, msg):
        self.logger.info(f"yt-dlp: {msg}")

    def warning(self, msg):
        self.logger.warning(f"yt-dlp: {msg}")

    def error(self, msg):
        self.logger.error(f"yt-dlp: {msg}")
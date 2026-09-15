import logging
import sys
import os
from datetime import datetime

def get_next_log_id(logs_dir):
    """Reads the last log ID from a hidden tracker file and increments it."""
    tracker_file = os.path.join(logs_dir, ".log_tracker")
    if os.path.exists(tracker_file):
        with open(tracker_file, "r") as f:
            try:
                current_id = int(f.read().strip())
            except ValueError:
                current_id = 0
    else:
        current_id = 0
    
    next_id = current_id + 1
    # Save the new ID back to the tracker
    with open(tracker_file, "w") as f:
        f.write(str(next_id))
        
    return next_id

def setup_logger():
    logger = logging.getLogger("YTDownloader")
    
    if not logger.handlers: # Prevent duplicate logs if initialized twice
        logger.setLevel(logging.DEBUG)
        log_format = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(threadName)-15s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 1. Create the 'logs' folder in the project root
        root_dir = os.path.dirname(os.path.dirname(__file__))
        logs_dir = os.path.join(root_dir, "logs")
        os.makedirs(logs_dir, exist_ok=True)

        # 2. Generate unique ID and Date/Time stamp
        log_id = get_next_log_id(logs_dir)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Format: Log_001_20260915_134741.log
        log_filename = f"Log_{log_id:03d}_{timestamp}.log"
        log_filepath = os.path.join(logs_dir, log_filename)

        # File Handler (Generates a brand new file for this specific session)
        file_handler = logging.FileHandler(log_filepath, mode='w', encoding='utf-8')
        file_handler.setFormatter(log_format)
        file_handler.setLevel(logging.DEBUG)

        # Console Handler (Prints to VS Code terminal)
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
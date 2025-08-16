# logger.py
import logging
import os
import sys
from logging.handlers import RotatingFileHandler

def setup_logging():
    try:
        user_home_dir = os.path.expanduser("~")
        log_dir = os.path.join(user_home_dir, "DevelopmentFiles")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "valorant_colorbot_log.txt")

        log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(module)s:%(lineno)d] - %(message)s')
        
        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8')
        file_handler.setFormatter(log_formatter)
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_formatter)
        console_handler.setLevel(logging.INFO)

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        
        if root_logger.hasHandlers():
            root_logger.handlers.clear()
            
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        logging.info("Logger setup complete. Logging to %s", log_file)

    except Exception as e:
        print(f"CRITICAL: Failed to configure logger: {e}", file=sys.stderr)

logger = logging.getLogger(__name__)
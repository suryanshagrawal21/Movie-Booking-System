import logging
import os
from datetime import datetime

class Logger:
    """Centralized logging utility for the application."""
    
    @staticmethod
    def setup_logger():
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        log_file = os.path.join("logs", f"app_{datetime.now().strftime('%Y-%m-%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger("MovieBookingSystem")

# Global logger instance
logger = Logger.setup_logger()

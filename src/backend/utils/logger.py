
import logging
from logging import StreamHandler, Formatter, FileHandler
import os
from datetime import datetime

today = datetime.today()
today_str = today.strftime("%Y-%m-%d-%H-%M-%S")
log_dir = "logs"

def get_logger(name: str) -> logging.Logger:
    """
    Create a logger with the specified name and optional log file.
    
    Args:
        name (str): The name of the logger.
        log_file (str, optional): The path to the log file. If not provided, logs will be printed to stdout.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create formatter
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create console handler
    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = FileHandler(os.path.join(log_dir, f"{today}.log"))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

if __name__=="__main__":
    # Example usage
    logger = get_logger(__name__)
    logger.info("This is an info message.")
    logger.error("This is an error message.")
    logger.debug("This is a debug message.")
    logger.warning("This is a warning message.")
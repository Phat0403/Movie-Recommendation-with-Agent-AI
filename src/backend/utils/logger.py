import logging
from logging import StreamHandler, Formatter, FileHandler
import os
from datetime import datetime

today = datetime.today()
today_str = today.strftime("%Y-%m-%d")
log_dir = "logs"

# Đảm bảo thư mục logs tồn tại
os.makedirs(log_dir, exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """
    Create a logger with the specified name and optional log file.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Tránh tạo lại handler nếu logger đã được cấu hình
    if logger.handlers:
        return logger

    # Định dạng log
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Ghi ra console
    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Ghi ra file với encoding UTF-8 (để tránh lỗi đọc ghi Unicode)
    log_file_path = os.path.join(log_dir, f"{today_str}.log")
    file_handler = FileHandler(log_file_path, encoding="utf-8")
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
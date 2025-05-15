import logging
from logging.handlers import RotatingFileHandler
import os

# Log directory and file config
LOG_DIR = "logs"
LOG_FILE = "app.log"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Create logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)  # تنظیم سطح پایه به DEBUG (همه لاگ‌ها ثبت می‌شن)

# Format for log messages
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] - %(message)s"
)

# Rotating File Handler
file_handler = RotatingFileHandler(
    filename=LOG_PATH,
    maxBytes=5 * 1024 * 1024,  # 5 MB
    backupCount=5,
    encoding='utf-8'  # پشتیبانی از فارسی در لاگ
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.INFO)

# Console Handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG)

# Avoid adding handlers multiple times in development (e.g., FastAPI reload)
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Optional shortcut if you want to use: from app.logger import get_logger
def get_logger(name: str = "app_logger") -> logging.Logger:
    return logging.getLogger(name)

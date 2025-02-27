import logging as sms_logging
import os

log_dir = "logs"
log_file = os.path.join(log_dir, "semaphore_api.txt")
os.makedirs(log_dir, exist_ok=True)

sms_logging.basicConfig(
    filename=log_file,
    level=sms_logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


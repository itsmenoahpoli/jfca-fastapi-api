import logging as mail_logging
import os

log_dir = "logs"
log_file = os.path.join(log_dir, "mail.txt")
os.makedirs(log_dir, exist_ok=True)

mail_logging.basicConfig(
    filename=log_file,
    level=mail_logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


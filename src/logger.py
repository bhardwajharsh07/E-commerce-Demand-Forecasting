import logging
import os
import socket
from datetime import datetime

DEVICE_NAME = socket.gethostname()

LOG_FILE = (
    f"{DEVICE_NAME}_"
    f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
)

logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)

LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] line %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
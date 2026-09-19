import logging
from pathlib import Path


LOG_FOLDER = Path("logs")
LOG_FOLDER.mkdir(exist_ok=True)

LOG_FILE = LOG_FOLDER / "app.log"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ecommerce_api")
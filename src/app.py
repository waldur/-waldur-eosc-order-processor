import logging

import utils

logging.getLogger("requests").setLevel(logging.WARNING)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s",
)


def sync_orders():
    utils.process_orders()
    logging.info("process_orders is finished.")
    return "The orders were synced"


if __name__ == "__main__":
    sync_orders()

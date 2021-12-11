import logging
import sys

from twitter import runner as twitter_runner
from csv_handler import runner as csv_runner

from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fmt = logging.Formatter("%(asctime)s %(levelname)-8s %(name)-30s %(message)s")
sh = logging.StreamHandler(sys.stderr)
sh.setFormatter(fmt)
logger.addHandler(sh)


def main():
    logger.info("Start Process")
    twitter_runner()
    # csv_runner()


if __name__ == "__main__":
    main()

import logging
import sys
import argparse

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
file_logger = logging.FileHandler("app.log")
logger.addHandler(file_logger)


RUNNERS = {
    "twitter": twitter_runner,
    "csv": csv_runner
}


def parse_cmd_args() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("runner")
    return vars(parser.parse_known_args()[0])


def main():
    logger.info("Start Process")
    args = parse_cmd_args()
    RUNNERS[args["runner"]]()


if __name__ == "__main__":
    main()

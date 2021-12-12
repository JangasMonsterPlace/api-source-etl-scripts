import logging
import os
import csv
import sys
from typing import Generator
from datetime import datetime
from dataclasses import dataclass
from common import settings, ORM
from common.domain_types import TransformedTextData
from time import sleep

from .gcp_storage import GCS


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fmt = logging.Formatter("%(asctime)s %(levelname)-8s %(name)-30s %(message)s")
sh = logging.StreamHandler(sys.stderr)
sh.setFormatter(fmt)
logger.addHandler(sh)
file_logger = logging.FileHandler("app.log")
logger.addHandler(file_logger)


@dataclass
class _SourceFileFormat:
    review_id: int
    rating: int
    created_at: str
    location: str
    text: str
    branch: str

    def parse(self) -> TransformedTextData:
        return TransformedTextData(
            source_id=str(self.review_id),
            source="csv",
            text=self.text,
            written_by_user_at=None if self.created_at == "missing" else datetime.strptime(self.created_at, "%Y-%m"),
            use_case=self.branch,
            sentiment=self.rating
        )


class _CsvRunner:
    def __init__(self):
        self.file_path = os.path.join(settings.BASE_DIR, "csv_handler", "data", "DisneylandReviews.csv")

    def extract_document(self) -> Generator[_SourceFileFormat, None, None]:
        for csv_file in GCS.get_files_from_blob(settings.GCP_STORAGE["primary_folder_name"]):
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                yield _SourceFileFormat(*row)

    def extract_and_transform_document(self) -> Generator[TransformedTextData, None, None]:
        for row in self.extract_document():
            yield row.parse()

    def etl(self):
        # Just for debug enable line below
        # GCS.upload_file(self.file_path)
        data = [
            tuple(row.__dict__.values())
            for row in self.extract_and_transform_document()
        ]
        if len(data) > 0:
            logger.info(f"Insert {len(data)} Rows into database")
            ORM.insert_transformed_review_data(data)
        else:
            logger.info("No data. Waiting ... ")


def runner():
    while True:
        try:
            csv_runner = _CsvRunner()
            csv_runner.etl()
        except Exception as e:
            logger.exception(str(e))
        sleep(1)

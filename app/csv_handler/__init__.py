import logging
import os
import csv
from typing import Generator
from datetime import datetime
from dataclasses import dataclass
from common import settings, ORM
from common.domain_types import TransformedTextData

logger = logging.getLogger(__name__)


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
            id=str(self.review_id),
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
        with open(self.file_path, mode="r") as csv_file:
            reader = csv.reader(csv_file)
            next(reader)
            for row in reader:
                 yield _SourceFileFormat(*row)

    def extract_and_transform_document(self) -> Generator[TransformedTextData, None, None]:
        for row in self.extract_document():
            yield row.parse()

    def etl(self):
        data = [
            tuple(row.__dict__.values())
            for row in self.extract_and_transform_document()
        ]
        ORM.insert_transformed_review_data(data)


def runner():
    csv_runner = _CsvRunner()
    csv_runner.etl()

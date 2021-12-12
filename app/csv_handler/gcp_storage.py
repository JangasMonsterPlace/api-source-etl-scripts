import logging
import os
from io import StringIO
from typing import Generator
from google.cloud import storage
from google.oauth2 import service_account
from google.cloud.storage.blob import Blob
from common import settings

logger = logging.getLogger(__name__)


_storage_client = storage.Client(
    credentials=service_account.Credentials.from_service_account_file(
        settings.GCP_STORAGE["credentials_file_path"]
    )
)

_bucket = _storage_client.get_bucket(settings.GCP_STORAGE["bucket_name"])


class GCS:
    @classmethod
    def get_files_from_blob(cls, prefix: str) -> Generator[bytes, None, None]:
        for blob in _bucket.list_blobs(prefix=prefix):
            if blob.name == f"{prefix}/":
                continue
            yield StringIO(blob.download_as_string().decode('utf-8'))
            cls.move_file(source_blob=blob)

    @staticmethod
    def move_file(source_blob: Blob):
        dest_blob_name = os.path.join(
            settings.GCP_STORAGE["backup_folder_name"],
            os.path.basename(source_blob.name)
        )
        _bucket.rename_blob(source_blob, dest_blob_name)

    @staticmethod
    def upload_file(path):
        blob = _bucket.blob(os.path.join("data", os.path.basename(path)))
        blob.upload_from_filename(path)

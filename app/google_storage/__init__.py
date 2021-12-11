import logging
from common import settings, storage_handler
from common.domain_types import TransformedTextData
from common.postgres import _db
import pandas as pd

logger = logging.getLogger(__name__)

class _gcs_loader:

    def __init__(self):

        self.primary_folder_name = settings.GCS_PRIMARY_FOLDER_NAME
        self.backup_folder_name = settings.GCS_BACKUP_FOLDER_NAME
        self.bucket_name        = settings.GCS_BUCKET_NAME
        self.engine = _db._engine()

    def etl(self):

        list_of_files = storage_handler.list_contents(prefix=self.primary_folder_name)

        list_of_files.remove(self.primary_folder_name + "/")

        if not list_of_files:

            print(f"No files found in {self.primary_folder_name} folder")

            return False

        for single_file_name in list_of_files:

            only_file_name = single_file_name.split("/")[-1].replace(".csv", "") # get only the file name

            file_path = f"gs://{self.bucket_name}/{single_file_name}"

            current_file_data = pd.read_csv(file_path) # pandas dataframe

            current_file_data.to_sql(only_file_name, self.engine, if_exists="replace", index=False)

        return True

    def move_to_backup(self):

        list_of_files = storage_handler.list_contents(prefix=self.primary_folder_name)

        list_of_files.remove(self.primary_folder_name + "/")

        for single_file_name in list_of_files:

            destination_blob_name = f"{self.backup_folder_name}/{single_file_name.split('/')[-1]}"

            source_blob = storage_handler.bucket.blob(single_file_name)

            blob_move = storage_handler.bucket.rename_blob(
                source_blob, destination_blob_name
            )

        return True

def runner():

    gcs_runner = _gcs_loader()

    gcs_runner.etl()

    gcs_runner.move_to_backup()

if __name__ == "__main__":

    runner()
from datetime import datetime
from typing import List
import os
from google.cloud import bigquery
from google.cloud.bigquery import QueryJob, QueryJobConfig
from google.cloud.bigquery.table import RowIterator
from google.cloud.exceptions import Conflict

from liquibase.dtos import DatasetChangelogDto
from liquibase.exceptions import ChangelogException, TooManyFilesException, FileQueryException
import logging


class DatasetChangelogDao:
    def __init__(self, dataset: str):
        qjc: QueryJobConfig = QueryJobConfig(default_dataset=f"{os.environ.get('PROJECT')}.{dataset}")
        self.client = bigquery.Client(default_query_job_config=qjc)
        self.dataset = dataset
        self.dcl = "datasetchangelog"
        self.destination = f"{self.client.project}.{self.dataset}.{self.dcl}"
        self.logger = logging.getLogger(__name__)

    def create_dataset(self, geographic_location: str):
        try:
            dataset_id = f"{self.client.project}.{self.dataset}"
            __dataset = bigquery.Dataset(dataset_id)
            __dataset.location = geographic_location
            self.client.create_dataset(__dataset)

            if self.__create_changelog() is False:
                raise ChangelogException("Could not create changelog table")
        except Conflict as e:
            self.logger.info(f"Dataset {self.dataset} already exists")

    def __create_changelog(self) -> bool:
        try:
            schema = [
                bigquery.SchemaField("file_name", "STRING", mode="REQUIRED"),
                bigquery.SchemaField("date_executed", "TIMESTAMP", mode="REQUIRED"),
                bigquery.SchemaField("md5sum", "STRING"),
            ]

            table = bigquery.Table(self.destination, schema=schema)
            self.client.create_table(table)
            self.logger.info(f"Created table {self.destination}")
            return True
        except Exception as e:
            self.logger.error(e)
            return False

    def get_recorded_file(self, file_name: str) -> DatasetChangelogDto:
        results = self.client.query(
            f"select * from `{self.destination}` WHERE file_name='{file_name}'").result()

        if results.total_rows == 0:
            return None

        if results.total_rows > 1:
            raise TooManyFilesException(f"{file_name} has more than one entry!")

        for r in results:
            return DatasetChangelogDto(file_name=r[0], md5sum=r[2])

    def insert_files_into_changelog(self, insert_records: List[DatasetChangelogDto]):
        rows_to_insert: List = []
        for record in insert_records:
            if not isinstance(record, DatasetChangelogDto):
                raise Exception("record is not type DatasetChangelogDto")

            rows_to_insert.append(
                (
                    record.filename,
                    datetime.now(),
                    record.md5sum
                )
            )

        try:
            if not len(rows_to_insert) == 0:
                table = self.client.get_table(self.destination)
                errors = self.client.insert_rows(
                    self.destination, rows_to_insert, selected_fields=table.schema
                )

                if errors is not None and len(errors) > 0:
                    raise Exception(errors)
        except Exception as e:
            error_message = "Failed to insert {} records into {}. Error: {}".format(
                len(insert_records), self.destination, e.args[0]
            )
            raise Exception(error_message)

    def execute_content(self, content):
        result: QueryJob = self.client.query(content)

        if result.errors is not None:
            errors: List[str] = [e["message"] for e in result.errors]

            if len(errors) > 0:
                raise FileQueryException(errors)

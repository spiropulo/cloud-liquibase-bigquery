import json
from typing import List

from liquibase.daos import DatasetChangelogDao
from liquibase.dtos import DatasetChangelogDto
from liquibase.exceptions import FileChangedException
from liquibase.utils import Utils


class Worker:
    def __init__(self, path_to_master_file: str = "bigquery/db/changelog_master.json", geographic_location: str = "US"):
        self.geographic_location = geographic_location
        self.master = json.load(open(path_to_master_file))
        self.dataset_dao = DatasetChangelogDao(self.master["dataset"])

    def initialize(self):
        self.__resolve_dataset()
        self.__resolve_files(self.master["files"])

    def __resolve_dataset(self):
        self.dataset_dao.create_dataset(geographic_location=self.geographic_location)

    def __resolve_files(self, files: List[str]):
        files_to_insert: List[DatasetChangelogDto] = list()
        for file_name in files:
            if self.__should_insert_file(file_name):
                files_to_insert.append(DatasetChangelogDto(file_name=file_name, md5sum=Utils.build_hash(file_name)))

        if len(files_to_insert) > 0:
            for f in files_to_insert:
                self.__execute(files=[f])
                self.dataset_dao.insert_files_into_changelog(insert_records=[f])

    def __should_insert_file(self, file_name) -> bool:
        dto: DatasetChangelogDto = self.dataset_dao.get_recorded_file(file_name)
        if dto is None:
            return True

        if dto.md5sum != Utils.build_hash(file_name=file_name):
            raise FileChangedException(f"File = {file_name}, has been changed! This filed was previously consumed.")

        return False

    def __execute(self, files: List[DatasetChangelogDto]):
        for f in files:
            content: str = open(f.filename, "r", encoding='utf-8').read()
            self.dataset_dao.execute_content(content=content)

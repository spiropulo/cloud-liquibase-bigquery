from typing import List
from unittest.mock import Mock

from tests.bdd.mocks.RowIteratorMock import RowIteratorMock


class ClientMock(Mock):
    project = "test_project"
    insert_changelog_count: int = 0
    executed_queries = list()
    available_responses: List[str] = list()

    def create_dataset(self, dataset):
        pass

    def create_table(self, table):
        pass

    def query(self, query):
        ClientMock.executed_queries.append(query)
        return self.__return_match_query(query=query)

    def insert_rows(self, table, rows, selected_fields=None, **kwargs):
        ClientMock.insert_changelog_count += 1

    def __return_match_query(self, query) -> RowIteratorMock:
        for ar in self.available_responses:
            if ar[0] in query:
                return RowIteratorMock([[ar[0], "SOMEDATE", ar[2]]])

        return RowIteratorMock([])

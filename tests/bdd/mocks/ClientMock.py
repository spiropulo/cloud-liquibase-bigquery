from unittest.mock import Mock

from tests.bdd.mocks.RowIteratorMock import RowIteratorMock


class ClientMock(Mock):
    project = "test_project"
    query_result: RowIteratorMock = None
    insert_changelog_count: int = 0
    executed_queries = list()

    def create_dataset(self, dataset):
        pass

    def create_table(self, table):
        pass

    def query(self, query):
        ClientMock.executed_queries.append(query)
        return ClientMock.query_result

    def insert_rows(self, table, rows, selected_fields=None, **kwargs):
        ClientMock.insert_changelog_count += 1
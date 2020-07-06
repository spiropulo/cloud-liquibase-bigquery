import unittest

from behave import *
from google.cloud import bigquery

from liquibase.utils import Utils
from liquibase.worker import Worker
from tests.bdd.mocks.ClientMock import ClientMock
from tests.bdd.mocks.DatasetMock import DatasetMock
from tests.bdd.mocks.RowIteratorMock import RowIteratorMock
from tests.bdd.mocks.TableMock import TableMock


class LiquibaseStep(unittest.TestCase):

    @given("changelog file location {path}")
    def files_location(context, path):
        context.path = path

    @when("I run")
    def i_run(context):
        Worker(path_to_master_file=context.path).initialize()

    @given("bigquery client mock")
    def bigquery_client_mock(context):
        bigquery.Client = ClientMock()
        bigquery.Dataset = DatasetMock()
        bigquery.Table = TableMock()

    @step("state of files are")
    def step_impl(context):
        values = list()
        for r in context.table:
            if r["exists"] == "True":
                values.append([r["file"], "somedate", Utils.build_hash(file_name=r["file"])])

        RowIteratorMock.values = values
        ClientMock.query_result = RowIteratorMock()

    @then("we confirm {count} files was inserted in the changelog table")
    def step_impl(context, count):
        assert ClientMock.insert_changelog_count == int(count)

    @then("we confirm the content of these files was executed")
    def step_impl(context):
        for r in context.table:
            content: str = open(r["file"], "r", encoding='utf-8').read()
            assert content in ClientMock.executed_queries

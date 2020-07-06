from typing import List
from unittest.mock import Mock


class RowIteratorMock(Mock):
    values: List[str] = list()

    def __iter__(self):
        return iter(RowIteratorMock.values)

    @property
    def total_rows(self):
        return len(RowIteratorMock.values)
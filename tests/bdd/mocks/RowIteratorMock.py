from typing import List


class RowIteratorMock:
    errors = None

    def __init__(self, values):
        self.values = values

    def __iter__(self):
        return iter(self.values)

    @property
    def total_rows(self):
        return len(self.values)

    def result(self):
        return RowIteratorMock(self.values)

    def errors(self):
        return RowIteratorMock.errors
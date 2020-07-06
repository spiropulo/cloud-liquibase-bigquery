from datetime import datetime


class DatasetChangelogDto:
    def __init__(self, file_name: str, md5sum: str):
        self.filename = file_name
        self.md5sum = md5sum
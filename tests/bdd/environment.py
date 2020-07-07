#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
from tests.bdd.mocks.ClientMock import ClientMock
from tests.bdd.mocks.RowIteratorMock import RowIteratorMock


def before_all(context):
    pass


def before_scenario(context: object, scenario: object) -> object:
    ClientMock.available_responses = list()
    ClientMock.insert_changelog_count = 0
    ClientMock.executed_queries = list()
    RowIteratorMock.errors = None



Feature: ETL Liquibase

  Background:
    Given bigquery client mock

  Scenario: Changelog is invoked for the first time.
    Given changelog file location tests/resources/bigquery_1/db/changelog_master.json
    And state of files are
      | file                                               | exists |
      | tests/resources/bigquery_1/db/files/initialize.sql | False  |
    When I run
    Then we confirm 1 files was inserted in the changelog table
    Then we confirm the content of these files was executed
      | file                                               |
      | tests/resources/bigquery_1/db/files/initialize.sql |

  Scenario: Run after initialization with same files, no files are inserted.
    Given changelog file location tests/resources/bigquery_1/db/changelog_master.json
    And state of files are
      | file                                               | exists |
      | tests/resources/bigquery_1/db/files/initialize.sql | True   |
    When I run
    Then we confirm 0 files was inserted in the changelog table

  Scenario: Changelog is invoked for the first time.
    Given changelog file location tests/resources/bigquery_2/db/changelog_master.json
    And state of files are
      | file                                               | exists |
      | tests/resources/bigquery_2/db/files/initialize.sql | True   |
      | tests/resources/bigquery_2/db/files/insert.sql     | False  |
      | tests/resources/bigquery_2/db/files/update.sql     | False  |
    When I run
    Then we confirm 2 files was inserted in the changelog table
    Then we confirm the content of these files was executed
      | file                                           |
      | tests/resources/bigquery_2/db/files/insert.sql |
      | tests/resources/bigquery_2/db/files/update.sql |
    
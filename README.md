# Python ETL Liquid Bigquery

This module provides a solution for applications that own **Bigquery** structures.
In stead of delegating controls to some third party systems like Terraform
or Cloud Formation PELB (Python ETL Liquid Bigquery) puts the jurisdiction in the
developers hands. PELB will target the current project defined by 
**GOOGLE_APPLICATION_CREDENTIALS** (DEV, STAGE, PROD, <BLAH>). 

## Index

This template repo starts with some examples:
* [View All Docs](./docs/)
* [Developer Setup](./docs/developer_setup.md)
* [Testing Strategy](./docs/testing_strategy.md)

## Project Structure

The project is structured with the following in mind:

- docs/
    - Documentation around the project
- project_template/
    - Operational source code exists here
- tests/bdd/
    - BDD feature testing with Behave and Gherkin feature files
- tests/resources/
    - Resources of various files types, exist here

## Prerequisites

Please ensure following the [Developer Setup](./docs/developer_setup.md) before developing \
for this project to ensure correct environment setup.

It is also suggested to view the [others docs as well](./docs/).

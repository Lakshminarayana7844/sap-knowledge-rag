# Databricks lakehouse basics

## Medallion layers
The medallion pattern stores data in bronze, silver and gold tables. Bronze keeps raw data, silver holds cleaned and conformed data, gold holds business level aggregates for reporting.

## Delta tables
Delta tables add ACID transactions, schema enforcement and time travel to files in cloud storage. Updates use MERGE for upserts.

## Unity Catalog
Unity Catalog governs tables, files and models with one permission model, lineage and audit logs across workspaces.

## Jobs
Databricks jobs schedule notebooks, Python scripts and pipelines. A task can depend on other tasks and retry on failure.

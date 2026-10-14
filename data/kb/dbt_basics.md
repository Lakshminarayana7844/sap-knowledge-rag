# dbt basics

## Models
A dbt model is a SELECT statement saved as a file. dbt builds it as a view or table in the warehouse and tracks dependencies with the ref function.

## Tests
Built in tests check that a column is unique, not null, has accepted values or matches a key in another model. Failed tests stop a build before bad data is used.

## Incremental models
An incremental model processes only new or changed rows on each run, which keeps large tables cheap to refresh.

## Documentation and lineage
dbt generates a documentation site with column descriptions and a lineage graph from the ref calls.

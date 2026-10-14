# Data quality in a warehouse

## Common checks
Typical checks are completeness, uniqueness of keys, valid value ranges, referential integrity and freshness. Run them after each load and before data reaches reports.

## Reconciliation
Reconciliation compares row counts and totals between the source and the warehouse. A difference after a delta load usually points to a missed request or a failed record.

## Handling failures
Quarantine bad records instead of dropping them silently. Keep the reason with the record so the source owner can correct it.

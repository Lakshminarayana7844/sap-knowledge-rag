# PySpark patterns

## DataFrames
A PySpark DataFrame is a distributed table. Transformations such as select, filter, join and groupBy are lazy. An action such as count or write triggers execution.

## Joins and skew
Broadcast a small table in a join to avoid a shuffle. If one key has far more rows than others the join is skewed, and salting the key spreads the load.

## Partitioning
Partition output by a column that is often used in filters, such as date. Too many small partitions slow reads, so aim for files of a few hundred megabytes.

## Window functions
Window functions compute running totals, ranks and lags per group without collapsing rows.

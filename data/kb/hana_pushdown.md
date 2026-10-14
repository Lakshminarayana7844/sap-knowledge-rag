# HANA push-down and modeling

## Code push-down
Code push-down means calculations run inside the SAP HANA database instead of the application server. Calculation views, SQL script routines and AMDP methods are common ways to do it.

## AMDP
An ABAP managed database procedure, AMDP, lets an ABAP class hold SQL script that runs in HANA. In BW/4HANA transformations an AMDP routine can replace a slow ABAP loop with set based SQL.

## Calculation views
A calculation view models joins, unions, aggregations and calculated columns in the database. Cube type views are used for analytics and dimension type views for master data.

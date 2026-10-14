# Advanced DataStore Object

## Purpose
The advanced DataStore Object, short aDSO, is the central persistence object in BW/4HANA. One aDSO can act as a staging area, a corporate memory or a reporting object, depending on how its settings are chosen.

## Settings and tables
An aDSO can have an inbound table, an active data table and a change log. Write-optimized settings keep only the inbound table. Standard settings add the active table and the change log so that deltas can be calculated.

## Activation
Data loaded into the inbound table is not visible for reporting in the standard setup until a request is activated. Activation moves records to the active table and writes before and after images to the change log.

## Delta handling
Downstream targets read the change log with a delta data transfer process. Only new requests since the last successful delta are transferred.

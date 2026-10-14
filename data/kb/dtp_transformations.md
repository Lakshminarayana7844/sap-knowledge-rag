# Transformations and DTP

## Transformation
A transformation maps source fields to target fields. It supports rules such as direct assignment, constants, formulas, lookups and routines written in ABAP.

## Data transfer process
A data transfer process, DTP, moves data from a source object to a target object using a transformation. A DTP can run in full mode or in delta mode.

## Error handling
Records that fail in a DTP can be written to an error stack. After the cause is fixed, the error DTP reloads only the failed records. This avoids reloading the whole request.

## Process chains
Process chains schedule loads, activation and housekeeping steps in order. A failed step stops the chain and raises an alert, so owners can repair and restart from that step.

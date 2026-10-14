# SAP Cloud Application Programming Model

## What CAP is
The SAP Cloud Application Programming Model, CAP, is a framework to build services in Node.js or Java. You describe data with CDS models and CAP generates the database schema and the service endpoints.

## CDS
Core Data Services models define entities, associations and services. A service definition exposes entities as an OData endpoint with filtering and paging out of the box.

## Local development
With the Node.js runtime a local SQLite database is used during development. The same model is later deployed to SAP HANA Cloud.

## Custom logic
Handlers attach to events such as before, on and after. Use a before handler to validate input and an after handler to enrich results.

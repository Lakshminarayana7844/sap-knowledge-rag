# BW/4HANA basics

## What BW/4HANA is
SAP BW/4HANA is a data warehouse product that runs only on the SAP HANA database. It replaces the older classic objects with a smaller set of modern ones and pushes calculations down to the database.

## Core objects
The main building blocks are the advanced DataStore Object (aDSO), the CompositeProvider, the Open ODS view and the InfoObject. Data flows through transformations and data transfer processes (DTP) from a source system into these objects.

## Layered architecture
A common design is the layered scalable architecture. Data lands in an acquisition layer, is harmonized in a corporate memory or propagation layer, and is shaped for reporting in an architected data mart layer.

# VFB update cycle for OWL files

## AIMS

* All owl entities referenced by VFB individuals files and queries should be checked for obsoletion status against originating ontologies at each update.  Any obsoleted or missing entities should be updated.
* OWL individual files should be regenerated as needed whenever the underlying DB is updated to incorporate new images or to improve annotation of existing images.
* Simple scripts should provide an easy way to add new individuals and OWL entities to the DB, singly or in bulk.

## Entity checking

The LMB mysql DB includes a central OWL_entity table for all OWL entities originating outside of VFB that are referenced in VFB queries or in axioms on individuals in VFB.  All entities referenced in axions on individuals are checked against this table, and an associated ontology table containing ontology and base URIs. During generation of individuals files, all external OWL entities referenced in axioms on individuals are checked against this table.  The module lmb\_fc\_tools.py contains the relevant functions.

The contents of the OWL entity table are checked against originating ontologies when these ontologies are updated.

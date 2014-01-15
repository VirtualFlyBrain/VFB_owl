# VFB update cycle for OWL files

## AIMS

* All owl entities referenced by VFB individuals files and queries should be checked for obsoletion status against originating ontologies at each update.  Any obsoleted or missing entities should be updated.
* OWL individual files should be regenerated as needed whenever the underlying DB is updated to incorporate new images or to improve annotation of existing images.
* Simple scripts should provide an easy way to add new individuals to the DB, singly or in bulk.

## Code

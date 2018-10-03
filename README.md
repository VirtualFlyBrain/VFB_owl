# VFB_owl

This repository is a home for the OWL files that are central to the VFB query system, and the scripts that generate these files.

WARNING - MOST OF THE CODE ON THIS REPO IS NOW DEPRECATED. The repository will likely be retired soon as it will be superceded by a version 2.0 of the VFB pipeline.

## Background & summary

The VFB query system relies on representation of data/knowledge in OWL.  Central to this a representation of Drosophila neuro-anatomy in the [Drosophila anatomy ontology](https://sourceforge.net/p/fbbtdv/wiki/Home/). The anatomical structures depicted in images displayed on VFB are represented as a [KnowledgeBase of OWL individuals](https://github.com/VirtualFlyBrain/VFB_owl/blob/master/doc/vfb_owl_ind_schema.md), which are classified (typed) using OWL class expressions referencing the anatomy ontology.  When this KnowledgeBase of individuals is combined with the ontology, a reasoner can be used to classify and query for anatomical structures depicted in the images on VFB.

The raw material for OWL individual files is a database developed and maintained at the LMB.  The scripts on this repository translate the information in this database into OWL for use on VFB.  To do this they use [Jython](http://www.jython.org/downloads.html) scripting over the [Brain library](https://github.com/loopasam/Brain/wiki), itself a facade over the OWL-API.

The LMB DB was originally developed for annotation and analysis of the FlyCircuit dataset and the structure of its oldest tables reflects this origin.  As we have added data from other sources, we have developed a more generalised schema as a set of parallel, linked tables.  As the old tables are in active use for annotation and NBlast cluster analysis they will remain in place for the forseable future.  This means that some subset of the scripts on this repository are likely to remain as one-offs dedicated only for generation of information on FlyCircuit individuals.   Others scripts aim to be generalizable to new content.

As well as scripts for writing OWL, this repo also contains scripts for writing to the LMB DB as well as for checking for the validity of ontology terms in the DB when an ontology used by VFB is updated.


 * [DB description](https://github.com/VirtualFlyBrain/VFB_owl/wiki/Individuals-DB)
 * [Code - env setup](https://github.com/VirtualFlyBrain/VFB_owl/blob/master/src/code)
 * [OWL generation code](https://github.com/VirtualFlyBrain/VFB_owl/tree/master/src/code/owl_gen)
 * [Code for adding to DB](https://github.com/VirtualFlyBrain/VFB_owl/tree/master/src/code/mod/lmb_fc_tools.py)
 * [Code for checking and updating OWL entities in DB](https://github.com/VirtualFlyBrain/VFB_owl/tree/master/src/code/entity_checks)



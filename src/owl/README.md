# OWL individuals files and the shell script for building and merging them.

datasets using generic build: Cachero2010', 'Ito2013', 'Jenett2012', 'Yu2013'  (listed in $DATASET).  
OWL files are named for the dataset

The FlyCircuit set + clusters is built separately and lives in flycircuit_plus.owl

vfb_ind.owl is a merged file containing the complete KnowledgeBase

fbbt_vfb_ind_pr_nr.owl is vfb_ind.owl + fbbt-non-classified.owl, pre-reasoned*, with redundancy removed.  
This combined file is used for live queries on VFB.

(*Pre-reasoning in this case instatiates non-redundant inferences on individuals as Type statements.  
This is important for display of Type statements in TermInfo for individuals on VFB.

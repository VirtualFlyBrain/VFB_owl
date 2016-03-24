## OWL individuals files + build script.

datasets using generic build: Cachero2010', 'Ito2013', 'Jenett2012', 'Yu2013'  (listed in $DATASET).  
OWL files are named for the dataset

The FlyCircuit set + clusters is built separately and lives in flycircuit_plus.owl

vfb_ind.owl is a merged file containing the complete KnowledgeBase

fbbt\_vfb\_ind\_pr\_nr.owl is vfb\_ind.owl + fbbt-non-classified.owl, pre-reasoned*, with redundancy removed.  
This combined file is used for live queries on VFB.

(*Pre-reasoning in this case instatiates non-redundant inferences on individuals as Type statements. This is required for complete for display of Type statements in TermInfo for individuals on VFB and for display of classification of individuals on results pages.)

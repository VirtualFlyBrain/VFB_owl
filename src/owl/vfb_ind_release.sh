#!/usr/bin/env bash

DATASETS=('Cachero2010' 'Ito2013' 'Jenett2012' 'Yu2013')

DSSTRING=''

cd ../code/owl_gen

for var in ${DATASETS[@]}
# java -classpath lib/*.jar:. my.package.Program
do
    echo $var
    java -cp $CP"*" org.python.util.jython vfb_ind_runner.py $USR $PD $var $FBBT
    DSSTRING+="--merge ${var}.owl "
done

java -cp $CP"*" org.python.util.jython fc_ind.py $USR $PD $FBBT

DSSTRING+="--merge flycircuit_plus.owl --merge flycircuit_direct_mappings.owl "

cd ../../owl
# # env should be moved to Jenkins job.  Should be actual list, with iteration deriving env with --merge in.

# # Merge ind files with specified release of fbbt
echo ''
echo "*** Merging ind files with $RELEASE version of fbbt ***"
owltools $FBBT --merge fb_features.owl --merge vfb_ext.owl $DSSTRING -o file://`pwd`/fbbt_vfb_ind.owl

# # assert inferences and strip out redundancy  # This 
echo ''
echo "*** Asserting inferences and striping redundancy ***"
owltools fbbt_vfb_ind.owl --reasoner elk --reasoner-ask-all --remove-indirect -a INDIVIDUALS -o -f ofn fbbt_vfb_ind_pr_nr.owl # Some special magic here. Best ask the owltools devs if you want to know how it works.

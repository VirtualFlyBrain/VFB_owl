#!/usr/bin/env bash

DATASETS=('Cachero2010' 'Ito2013' 'Jenett2012' 'Yu2013')

DSSTRING=''

cd ../code/owl_gen

ERROR_SUMMARY=""
for var in ${DATASETS[@]}
# java -classpath lib/*.jar:. my.package.Program
do
    echo $var
    ./vfb_ind_runner.py $USR $PD $var $FBBT
    DSSTRING+="--merge ${var}.owl "
    echo "Return stat: "$?
done

./fc_ind.py $USR $PD $FBBT
echo "Return stat: "$?

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
owltools fbbt_vfb_ind.owl --reasoner elk --reasoner-ask-all --remove-indirect -a INDIVIDUALS -o fbbt_vfb_ind_pr_nr.owl # Some special magic here. Best ask the owltools devs if you want to know how it works.
echo ''
echo "***Building file for SOLR loading ***"
echo ''

owltools fbbt_vfb_ind_pr_nr.owl --reasoner elk --assert-inferred-subclass-axioms --removeRedundant -o fbbt_vfb_ind_prc_nr.owl

./DL2subset.py fbbt_vfb_ind_prc_nr.owl



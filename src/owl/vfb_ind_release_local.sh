#!/usr/bin/env bash

DATASETS=('Cachero2010' 'Ito2013' 'Jenett2012' 'Yu2013' 'JenettShinomya_BrainName')

DSSTRING=''

cd ../code/owl_gen

# Generate new set of feature classes from FlyBase

echo ''
echo 'Building ontology of FlyBase features'

./fb_feat_ont_gen.py $USR $PD
echo "Return stat: "$?

ERROR_SUMMARY=""
for var in ${DATASETS[@]}
# java -classpath lib/*.jar:. my.package.Program
do
    echo "Building "$var
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
owltools fbbt_vfb_ind_prc_nr.owl --set-ontology-id -v 'http://purl.obolibrary.org/obo/fbbt/vfb/'$v'vfb.owl' 'http://purl.obolibrary.org/obo/fbbt/vfb/vfb.owl' -o vfb.owl

# Running reporting tests on build

export p=`pwd`

cd ../code/unit_tests

./query_test_mod.py $p'/fbbt_vfb_ind_prc_nr.owl' > $p'/test_results.txt'

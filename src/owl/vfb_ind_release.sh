#!/usr/bin/env bash

# env should be moved to Jenkins job.  Should be actual list, with iteration deriving env with --merge in.
export IND_FILES="--merge Cachero2010.owl --merge Ito2013.owl --merge Jenett2012.owl --merge Yu2013.owl --merge flycircuit_plus.owl --merge flycircuit_direct_mappings.owl"
export RELEASE="2014-01-29"

# Merge ind files with specified release of fbbt
echo ''
echo "*** Merging ind files with $RELEASE version of fbbt ***"
owltools http://purl.obolibrary.org/obo/fbbt/${RELEASE}/fbbt-non-classified.owl --merge fb_features.owl $IND_FILES -o file://`pwd`/fbbt_vfb_ind.owl

# assert inferences and strip out redundancy  # This 
echo ''
echo "*** Asserting inferences and striping redundancy ***"
owltools fbbt_vfb_ind.owl --reasoner elk --reasoner-ask-all --remove-indirect -a INDIVIDUALS -o fbbt_vfb_ind_pr_nr.owl # Some special magic here. Best ask the owltools devs if you want to know how it works.

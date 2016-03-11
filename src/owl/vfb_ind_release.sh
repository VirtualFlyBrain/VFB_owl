#!/usr/bin/env bash

## Lib setup for this job - Use maven (pom.xml in vfb_owl repo root)
### $CP = full classpath with Jython JAR and rqd JAVA libs
## The following VARS must be set before runnning this job
### $USR, $PD = mySQL DB credentials (DB connection requires ssh tunnel using shared key)
### $FBBT = full path to local copy of fbbt-non-classified.owl - of appropriate version.
### The following files must be present

### Repo file structure:
# lib/
# src/owl/{build script and OWL files live here}
# src/code/mod local Jython mods
# src/code/owl_build Jython build scripts



exit_on_fail() { 
    status=$1
    message=$2
    if [ "$status" != 0 ];
    then echo "$message" " failed with exit status: " "$status:" ; exit 1;
    else echo "$message successful";
    return 0;
    fi
}

progress_chat() {
    echo ''
    echo "*** $@ ***"
}

# Edit this to add additional datasets
DATASETS=('Cachero2010' 'Ito2013' 'Jenett2012' 'Yu2013' 'JenettShinomya_BrainName')

DSSTRING=''


cd ../code/owl_gen
# job='Building ontology of FlyBase features';
# progress_chat "$job";
# java -Xmx6000m -cp $CP"*" org.python.util.jython fb_feat_ont_gen.py $USR $PD
# exit_on_fail $? "$job"

for var in ${DATASETS[@]}
# java -classpath lib/*.jar:. my.package.Program
do
    job="Building $var inds";
    progress_chat $job
    java -Xmx6000m -cp $CP"*" org.python.util.jython vfb_ind_runner.py $USR $PD $var $FBBT
    DSSTRING+="--merge ${var}.owl "
    exit_on_fail $? "$job"
done

job="Adding analysis results to flycircuit neuron inds.";
progress_chat $job
java -Xmx6000m -cp $CP"*" org.python.util.jython fc_ind.py $USR $PD $FBBT
exit_on_fail $? $job

DSSTRING+="--merge flycircuit_plus.owl --merge flycircuit_direct_mappings.owl "

cd ../../owl
# # env should be moved to Jenkins job.  Should be actual list, with iteration deriving env with --merge in.

# # Merge ind files with specified release of fbbt
job="Merging ind files with ${FBBT}" 
progress_chat $job
owltools $FBBT --merge fb_features.owl --merge vfb_ext.owl --merge vfb_license_and_attribution.owl $DSSTRING -o file://`pwd`/fbbt_vfb_ind.owl
exit_on_fail $? $job

# # assert inferences and strip out redundancy  # This
job="Asserting inferences and striping redundancy" 
progress_chat $job
owltools fbbt_vfb_ind.owl --reasoner elk --reasoner-ask-all --remove-indirect -a INDIVIDUALS -o fbbt_vfb_ind_pr_nr.owl # Some special magic here. Best ask the owltools devs if you want to know how it works.
exit_on_fail $? $job

$v = `date "+%Y-%m-%d"`
$job="Setting IRI + version IRI using current date "$v
progress_chat $job
# Ideally would save as functional syntax, but bug in owltools preventing this.
owltools fbbt_vfb_ind_prc_nr.owl --set-ontology-id -v 'http://purl.obolibrary.org/obo/fbbt/vfb/'$v'vfb.owl' 'http://purl.obolibrary.org/obo/fbbt/vfb/vfb.owl' -o vfb.owl
exit_on_fail $? $job

$job="Compressing"
progress_chat $job
gzip -c vfb.owl > vfb.owl.gz
exit_on_fail $? $job

export p=`pwd`

cd ../code/unit_tests

$job="Running reporting tests on build"
progress_chat $job
./query_test_mod.py $p'/vfb.owl' > $p'/test_results.txt'
exit_on_fail $? $job



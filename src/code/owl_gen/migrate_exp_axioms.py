#!/usr/bin/env jython

from uk.ac.ebi.brain.core import Brain
from owl2pdm_tools import migrate_axioms_to_ind
import sys
import time
                

eont = Brain("http://purl.obolibrary.org/obo/vfb/", "http://purl.obolibrary.org/obo/vfb/expression_pattern_ind.owl")
eont.learn(sys.argv[1]) # assuming class & individual files loaded separately.
eont.learn(sys.argv[2]) # 


# Find all expression classes

exp = eont.getSubClasses("B8C6934B-C27C-4528-BE59-E75F5B9F61B6", 0) # SC of expression pattern

# Iterate over expression pattern classes, migrating all subclass axioms to their instances.
start = time.time()
for e in exp:
    print time.time() - start # for debugging speed.
    start = time.time()
    migrate_axioms_to_ind(eont, e)

eont.save("../../owl/Jenett2012_full.owl")
eont.sleep()




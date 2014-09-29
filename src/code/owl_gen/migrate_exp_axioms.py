#!/usr/bin/env jython

from uk.ac.ebi.brain.core import Brain
from owltools.graph import OWLGraphWrapper
import sys
#import time
import re

# Aim:

# Take class level assertions and instantiate individual level axioms.

## Hmmm - might be hard...

### Example we already have a VFB individual  'X expression pattern from ...' and a class for X expression pattern.  One is inferred or asserted to be a member of the other.  The class has a bunch of overlaps axioms on it that we want to move down to the individual level.  Assume no inference needed - all axioms we want are directly on this class.

## - Could simply use OWLtools GraphWrapper to find relevant axioms.  Then use Brain to add them to the individual.


def migrate_axioms_to_ind(cogw, classId, ind, indId):
    # Check that ind really is member of class 
    owlClass = cogw.getOWLClassByIdentifier(classId) # Seems to want an OBO ID!  # Really need to get around this - ask Chris & Heiko
    edges = cogw.getOutgoingEdges(owlClass)
    for edge in edges:
        property_list = edge.getQuantifiedPropertyList()
        if len(property_list) == 1: # Ignore complex axioms
            rel = property_list[0]
            relid = re.sub(':', '_', cogw.getIdentifier(rel))
            obj = edge.getTarget()
            cid = re.sub(':', '_', cogw.getIdentifier(obj))
            if rel.isSubClassOf():
                # get ID (as OWL)
                ind.Type(indId, cid)
            else:
                typ = "%s some $s" % (relid, cid)
                ind.Type(indId, typ)
    


eont = Brain("http://purl.obolibrary.org/obo/vfb/", "http://purl.obolibrary.org/obo/vfb/expression_pattern_ind.owl")
eont.learn(sys.argv[1]) # assuming class & individual files loaded separately.
eont.learn(sys.argv[2]) # 
eonto = eont.getOntology()
eogw = OWLGraphWrapper(eonto)

## For inds

#ind = Brain("http://purl.obolibrary.org/obo/vfb", "http://purl.obolibrary.org/obo/vfb/expression_pattern_ind.ow")


# Iterate over all expression classes, finding individuals

exp = eont.getSubClasses("B8C6934B-C27C-4528-BE59-E75F5B9F61B6", 0) # SC of expression pattern

# Double loop makes this very slow. Even more so with loop in function.

#start = time.time()
for e in exp:
    #print time.time() - start # for debugging speed.
    #start = time.time()
    members = eont.getInstances(e, 0)
    for m in members:
        migrate_axioms_to_ind(eogw, e, eont, m)

eont.save("../../owl/expression_pattern_ind.owl")
eont.sleep()




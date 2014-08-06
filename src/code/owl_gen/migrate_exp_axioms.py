from uk.ac.ebi.brain.core import Brain
from owltools.graph import OWLGraphWrapper

# Aim:

# Take class level assertions and instantiate individual level axioms.

## Hmmm - might be hard...

### Example we already have a VFB individual  'X expression pattern from ...' and a class for X expression pattern.  One is inferred or asserted to be a member of the other.  The class has a bunch of overlaps axioms on it that we want to move down to the individual level.  Assume no inference needed - all axioms we want are directly on this class.

## - Could simply use OWLtools GraphWrapper to find relevant axioms.  Then use Brain to add them to the individual.


def migrate_axioms_to_ind(cogw, classId, ind, indId):
    # Check that ind really is member of class
    ###
    owlClass = cogw.getOWLClassByIdentifier(classId) # Seems to want an OBO ID!
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
    


eont = Brain()
eont.learn(URL)
eonto = eont.getOntology()
eogw = OWLGraphWrapper(eonto)

## For inds

ind = Brain()
ind.learn(URL)

# Iterate over all expression classes, finding individuals

exp = eont.getSubClasses(, 0) # SC of expression pattern

for e in exp:
    members = cont.getIndividuals(e)
    for m in members:
        migrate_axioms_to_in(eogw, e, ind, m)



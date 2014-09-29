from org.semanticweb.owlapi.apibinding import OWLManager
from org.semanticweb.owlapi.model import IRI

def typeAxioms2pdm(iri_string, ont):
    
    """iri_string: An iri string referencing an individual
     ont: An owlAPI ontology object for an ontology that includes the referenced individual
     Returns a python datamodel consisting of a list of dicts with keys: 
     isAnonymous:boolean; 
     relId:URI_string; 
     objectId:URI_string.
     """ 
     
    # May be better to operate on only short form IDs.
    
    iri = IRI.create(iri_string)
    # iri_string is an OWLIndividual iri string
    # ont is an ontology object
    
    manager = OWLManager.createOWLOntologyManager()
    factory = manager.getOWLDataFactory()
    i = factory.getOWLNamedIndividual(iri)
    
    out = [] # Output array
    types = i.getTypes(ont) # This has type  <type 'java.util.TreeSet'>, but can be iterated over as if it were a list of class expression axioms objects
    for t in types:
        od = {}
        if t.isAnonymous():
            od['isAnonymous'] = True
            classes = t.getClassesInSignature()
            # Need something in here to check for > 1 class in sig!
            for claz in classes:
                od['objectId'] = claz.toStringID()
            ops = t.getObjectPropertiesInSignature()
            for op in ops:
                od['relId'] = op.toStringID()
            out.append(od)
        else:
            od['isAnonymous'] = False
            classes = t.getClassesInSignature()
            out.append(od)
    return out

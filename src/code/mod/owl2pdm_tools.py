from org.semanticweb.owlapi.apibinding import OWLManager
from org.semanticweb.owlapi.model import IRI
from org.semanticweb.owlapi.util import SimpleShortFormProvider
import warnings


def get_types_for_ind(iri_string, ont):
    """iri_string: An iri string referencing an individual
    ont: An owlAPI ontology object for an ontology that 
    includes the referenced individual.
    Returns and iterable set of class expressions
    """
        
    iri = IRI.create(iri_string)    
    manager = OWLManager.createOWLOntologyManager()
    factory = manager.getOWLDataFactory()
    i = factory.getOWLNamedIndividual(iri)
    return i.getTypes(ont) # 

class simpleClassExpression():
    """Takes an OWL API classExpression as arg.
    Checks whether, if anonymous, it consists of
     just one op and one class.
     """     
     
    def __init__(self, classExpression):
        self.ce = classExpression
        self.classes = list(self.ce.getClassesInSignature())
        self.rels = list(self.ce.getObjectPropertiesInSignature())
        self._test_simplicity()
        
    def _test_simplicity(self):
        """Tests whether, if anonymous, there is only one object property and one class."""
        #Ideally would also check quantifier
        if not self.ce.isAnonymous():
            if len(self.rels) > 1:
                warnings.warn("Class expression, %s, too complex to process" % self.ce)
            if len(self.classes) > 1:
                warnings.warn("Class expression, %s, too complex to process" % self.ce)
    
    def get_class_sfid(self):
        """Returns a shortFormId for the class in the simple class expression"""
        ssfp = SimpleShortFormProvider()
        return ssfp.getShortForm(self.classes[0])
        
    def get_rel_sfid(self):
        """Returns a shortFormId for the relation (OP) in the simple class expression"""
        ssfp = SimpleShortFormProvider()
        return ssfp.getShortForm(self.rels[0])
        
    


def typeAxioms2pdm(iri_string, ont):
    
    """iri_string: An iri string referencing an individual
     ont: An owlAPI ontology object for an ontology that includes the referenced individual
     Returns a python datamodel consisting of a list of dicts with keys: 
     isAnonymous:boolean; 
     relId:URI_string; 
     objectId:URI_string.
     """
#     Would be better if could take sfid
     
    types = get_types_for_ind(iri_string, ont)    
    out = [] # Output array
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

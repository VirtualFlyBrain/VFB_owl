from org.semanticweb.owlapi.apibinding import OWLManager
from org.semanticweb.owlapi.model import IRI
from org.semanticweb.owlapi.util import SimpleShortFormProvider
from org.semanticweb.owlapi.util import BidirectionalShortFormProviderAdapter
from java.util import TreeSet

import warnings


class simpleClassExpression():
    """Takes an OWL API classExpression as arg.
    Checks whether, if anonymous, it consists of
     just one op and one class.
     """     
     
    def __init__(self, classExpression):
        self.ce = classExpression
        self.classes = list(self.ce.getClassesInSignature())
        self.rels = list(self.ce.getObjectPropertiesInSignature())
        self.is_simple()
        
    def is_simple(self):
        """Tests whether, if anonymous, there is only one object property and one class."""
        #Ideally would also check quantifier
        if self.ce.isAnonymous():
            if len(self.rels) > 1:
                warnings.warn("Class expression, %s, too complex to process" % self.ce)
                return False
                raise
        if len(self.classes) > 1:
            warnings.warn("Class expression, %s, too complex to process" % self.ce)
            return False
            raise
        else:
            return True  
    
    def get_class_sfid(self):
        """Returns a shortFormId for the class in the simple class expression"""
        ssfp = SimpleShortFormProvider()
        return ssfp.getShortForm(self.classes[0])
        
    def get_rel_sfid(self):
        """Returns a shortFormId for the relation (OP) in the simple class expression"""
        ssfp = SimpleShortFormProvider()
        return ssfp.getShortForm(self.rels[0])
    
    def get_sce_pdm(self):
        od = {}
        if self.ce.isAnonymous():
            od['isAnonymous'] = True
            od['relId'] = self.get_rel_sfid()
        else:
            od['isAnonymous'] = False
        od['objectId'] = self.get_class_sfid()
        return od
    
    def get_sce_as_manchester(self):
        if not self.ce.isAnonymous():
            return self.get_class_sfid()
        else:
            return "%s some %s" % (self.get_rel_sfid(), self.get_class_sfid())

class ont_manager():
    # I seem to be reinventing Brain....
    """Constructors: ont_manager(OWLontology)
       Attributes:
           ont
           manager: OWLManager
           factory: OWLDataFactory
           simple_sfp: uses getShortForm(IRI, iri)
           bi_sfp: uses .getEntity(<string> shortForm), .getShortForm(OWLEntity entity)
           """
        
    def __init__(self, ont, file_path=''):
        self.ont = ont
        self.manager = OWLManager.createOWLOntologyManager()
        self.factory = self.manager.getOWLDataFactory()
        self.simple_sfp = SimpleShortFormProvider() # .getShortForm(iri)
        ontset = TreeSet()
        ontset.add(ont)
        #public BidirectionalShortFormProviderAdapter(OWLOntologyManager man,
        #java.util.Set<OWLOntology> ontologies,
        #ShortFormProvider shortFormProvider) # Providing the manager, means that this listens for changes.
        self.bi_sfp = BidirectionalShortFormProviderAdapter(self.manager, ontset, self.simple_sfp) # .getShortForm(iri); .getEntity()
    
    def get_ind_from_iri(self, iri_string):
        iri = IRI.create(iri_string)
        return self.factory.getOWLNamedIndividual(iri)
        
    def get_types_for_ind(self, iri_string = '', sfid = ''):
        """iri_string: An iri string referencing an individual
        ont: An owlAPI ontology object for an ontology that 
        includes the referenced individual.
        Returns an iterable set of class expressions
        """
        # Could refactor to generic get owl entity fn.
        i = ''
        if sfid:
            i = self.bi_sfp.getEntity(sfid)
        elif  iri_string:
            i = self.get_ind_from_iri(iri_string)
        else:
            warnings.warn("Method requires either iri string or shortFormID to be specified")
        return i.getTypes(self.ont) # 
    
    def get_axioms_ref_class(self, iri_string):
        """Returns all axioms referencing a class."""
        iri = IRI.create(iri_string)    
        c = self.factory.getOWLClass(iri)
        return c.getReferencingAxioms(self.ont)#? 

    def get_sc_axioms_on_class(self, iri_string = '', sfid =''):
        """Returns an interable set of asserted superclasses of class."""
        c = ''
        if sfid:
            c = self.bi_sfp.getEntity(sfid)
        else:
            iri = IRI.create(iri_string)    
            c = self.factory.getOWLClass(iri)
        return c.getSuperClasses(self.ont)#?
    
    def get_version_iri(self):
        """Wot is says on' tin.  Returns string"""
        oid = self.ont.get_id()
        version_iri = oid.getVersionIRI()
        return version_iri.toString()    
    
    def typeAxioms2pdm(self, iri_string = '', sfid = ''):
    
        """iri_string: An iri string referencing an individual
        ont: An owlAPI ontology object for an ontology that includes the referenced individual
        Returns a python datamodel consisting of a list of dicts with keys: 
        isAnonymous:boolean; 
        relId:URI_string; 
        objectId:URI_string.
        """
        
        types = self.get_types_for_ind(iri_string = iri_string, sfid = sfid)    
        out = [] # Output array
        for t in types:
            sce = simpleClassExpression(t)
            if sce.is_simple():
                out.append(sce.get_sce_pdm())
        return out
    
    def getAllObjectProperties(self):
        """Returns a list of object Property sfids"""
        ### A good candidate for addition to Brain
        out = []
        for r in self.ont.getObjectPropertiesInSignature():
            out.append(self.simple_sfp.getShortForm(r))
        return out
    
def migrate_axioms_to_ind(brain, claz):
    """Finds all instances of a specified class, and migrates asserted
    subclassing axioms down from the specified class to the individuals found."""
    exp_pat_inds = brain.getInstances(claz, 0)
    onto = brain.getOntology()
    om = ont_manager(onto)
    # get an iterable set of axioms
    sc_ax = om.get_sc_axioms_on_class(sfid = claz)
    for i in exp_pat_inds:
        for ax in sc_ax:
            sce = simpleClassExpression(ax)
            # Should really do this with a native owl-api method...
            brain.type(sce.get_sce_as_manchester(), i)
    

# Keeping these as a separate free standing function for now, until dependent scripts refactored
def get_types_for_ind(iri_string, ont):
    """iri_string: An iri string referencing an individual
    ont: An owlAPI ontology object for an ontology that 
    includes the referenced individual.
    Returns and iterable set of class expressions
    """
    # Could refactor to generic get owl entity fn.
     
    iri = IRI.create(iri_string)
    manager = OWLManager.createOWLOntologyManager()
    factory = manager.getOWLDataFactory()
    i = factory.getOWLNamedIndividual(iri)
    return i.getTypes(ont) # 


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

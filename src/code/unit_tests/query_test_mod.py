#!/usr/bin/env Jython -J-Xmx8000m

from uk.ac.ebi.brain.core import Brain
from tsv2pdm import tab
import sys
import warnings

# Draft class for object-based unit test system.  This allows more info to be stored about queries and tests. Objects should be populated from a tsv.  Good potential for generating documentation straight from tsv or by using these objects...

class Query:
    """Class for testing queries against ontology + individuals files for VFB
    Attributes:
        query - DL query with shortFormIDs
        query_by_label - DL query with labels (for reference)
        query_text - Descriptive text for web-page / doc.
        description -  # Why is this test being run?    query = '' # DL query with shortFormIDs
        i = False # Should it have instances? - Default = False
        s = True  # should it have subclasses? - Default = True
    Methods:
        qtest - 
    """  
    def __init__(self, query, ont): 
        "Query,Query_by_label,SubClasses,Instances,Test_Justification,Website Text,Page"
        self.ont = ont
        self.query = query['Query']
        self.query_by_label = query['Query_by_label']# DL query with labels (for reference)
        self.query_text = ''  # Descriptive text for web-page / doc.
        self.description = ''  # Why is this test being run?
        self.i = int(query['Instances']) # Should it have instances? - Default = False
        self.s = int(query['SubClasses'])   # should it have subclasses? - Default = True
        
    def qtest(self):
        qstat = 1
        """Method to run test queries on object.
        Uses s, i boolean attributes to decide whether to run SubClassOf &/or Individuals queries respectively.
        Warns if no results returned or prints number of results returned
        If any query returns no results, this method returns false, otherwise is returns true.
        """
        if self.i:
            instances = self.ont.getInstances(self.query, 0)
            if instances:
                print self.query_by_label + " - Individuals: " + str( len(instances) )
            else:
                warnings.warn(self.query_by_label + " has no instances!")
                qstat = 0
        if self.s:
            subclasses = self.ont.getSubClasses(self.query, 0)
            if subclasses:
                print self.query_by_label + " - subClasses: " + str( len(subclasses) )
            else:    
                warnings.warn(self.query_by_label + " has no subclasses!")
                qstat = 0
        return qstat
                
                
def __main__():
    ont = Brain()
    ont.learn(sys.argv[1])
    qtab = tab("./", "queries.tsv") 
    for r in qtab.tab:
        q = Query(r, ont)
        q.qtest()
    ont.sleep()
__main__()
                # With object-based system, where should the details live?  Better to make a separate config table and have this script read it in.
                # TODO - write tsv parser + procedural code to generate objects and run tests.

# Unit tests using dict.

# DL_QueriesByID = {}
# 
# DL_QueriesByID['FBbt_00005106 that RO_0002131 some FBbt_00003624'] = "neuron that overlaps some 'adult brain'"
# DL_QueriesByID['FBbt_00005106 that RO_0002113 some FBbt_00003624'] = "neuron that has_presynaptic_terminal_in some 'adult brain'"
# DL_QueriesByID['FBbt_00005106 that RO_0002130 some FBbt_00003624'] = "neuron that has_postsynaptic_terminal_in some 'adult brain'"
# DL_QueriesByID['FBbt_00005106 that RO_0002110 some FBbt_00003624'] = "neuron that has_synaptic_terminal_in some 'adult brain'"
# DL_QueriesByID['FBbt_00005099 that RO_0002134 some FBbt_00003624'] = "neuron projection bundle' that innervates some 'adult brain'"
# DL_QueriesByID['FBbt_00007683 that RO_0002131 some FBbt_00003624'] = "'neuroblast lineage clone' that overlaps some 'adult brain'"
# DL_QueriesByID['FBbt_00005106 that RO_0002101 some FBbt_00005099'] = "neuron that fasciculates_with some 'neuron projection bundle'"
# DL_QueriesByID['FBbt_00005106 that BFO_0000050 some FBbt_00007683'] = "neuron that part_of some 'neuroblast lineage clone'"
# 
# 
# for Q, qtext in DL_QueriesByID.iteritems():
#     instances = vfb_ind.getInstances(Q, 0)
#     if instances:
#         print qtext + " - Individuals: " + str( len(instances) )
#     else:
#         warnings.warn(qtext + " has no instances!")
#     instances = vfb_ind.subClasses(Q, 0)
#     if subclasses:
#         print qtext + " - subClasses: " + str( len(subclasses) )
#     else:
#         warnings.warn(qtext + " has no subclasses!")
# 
#         # Queries for individuals currently work on labels.  Unusually, the
# 
# # roll name_id lookup
# 
# name_id = {}
# I = vfb_ind.getInstances("Thing", 0)
# S = vfb_ind.SubClassOf("Thing", 0)
# 
# while i in I:
#     name_id[vfb_ind.getLabel(i)] = i
#     
# while s in S:
#     name_id[vfb_ind.getLabel(s)] = s
# 
# cluster = name_id['cluster']
# neuron = name_id['neuron']
# 
#     # But how to get a list of object properties?
    
        
        # How to structure this? need lookup by ID.




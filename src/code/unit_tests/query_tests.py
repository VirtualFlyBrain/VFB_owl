#!/usr/bin/env Jython -J-Xmx8000m

from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
import warnings

vfb_ind = Brain()
vfb_ind.learn("../../owl/fbbt_vfb_ind_pr_nr.owl")

# Draft object-based unit test system. This should be populated from a spreadsheet.
class Query:
    query = ''
    query_text = ''
    i = False # Should it have instances?
    s = True  # should it have subclasses?
    def qtest(self, ont):
        if self.i:
            instances = ont.getInstances(self.query, 0)
            if instances:
                print qtext + " - Individuals: " + str( len(instances) )
            else:
                warnings.warn(qtext + " has no instances!")
        if self.s:
            if subclasses:
                print qtext + " - subClasses: " + str( len(subclasses) )
            else:
                warnings.warn(qtext + " has no subclasses!")

        

# Unit tests using dict.

DL_QueriesByID = {}

DL_QueriesByID['FBbt_00005106 that RO_0002131 some FBbt_00003624'] = "neuron that overlaps some 'adult brain'"
DL_QueriesByID['FBbt_00005106 that RO_0002113 some FBbt_00003624'] = "neuron that has_presynaptic_terminal_in some 'adult brain'"
DL_QueriesByID['FBbt_00005106 that RO_0002130 some FBbt_00003624'] = "neuron that has_postsynaptic_terminal_in some 'adult brain'"
DL_QueriesByID['FBbt_00005106 that RO_0002110 some FBbt_00003624'] = "neuron that has_synaptic_terminal_in some 'adult brain'"
DL_QueriesByID['FBbt_00005099 that RO_0002134 some FBbt_00003624'] = "neuron projection bundle' that innervates some 'adult brain'"
DL_QueriesByID['FBbt_00007683 that RO_0002131 some FBbt_00003624'] = "'neuroablast lineage clone' that overlaps some 'adult brain'"
DL_QueriesByID['FBbt_00005106 that RO_0002101 some FBbt_00005099'] = "neuron that fasciculates_with some 'neuron projection bundle'"
DL_QueriesByID['FBbt_00005106 that BFO_0000050 some FBbt_00007683'] = "neuron that part_of some 'neuroblast lineage clone'"


for Q, qtext in DL_QueriesByID.iteritems():
    instances = vfb_ind.getInstances(Q, 0)
    if instances:
        print qtext + " - Individuals: " + str( len(instances) )
    else:
        warnings.warn(qtext + " has no instances!")
    instances = vfb_ind.subClasses(Q, 0)
    if subclasses:
        print qtext + " - subClasses: " + str( len(subclasses) )
    else:
        warnings.warn(qtext + " has no subclasses!")



# roll name_id lookup

name_id = {}
I = vfb_ind.getInstances("Thing", 0)
S = vfb_ind.SubClassOf("Thing", 0)

while i in I:
    name_id[vfb_ind.getLabel(i)] = i
    
while s in S:
    name_id[vfb_ind.getLabel(s)] = s

cluster = name_id['cluster']
neuron = name_id['neuron']

    # But how to get a list of object properties?
    
        
vfb_ind.sleep()
        # How to structure this? need lookup by ID.




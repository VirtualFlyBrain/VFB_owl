#!/usr/bin/env jython -J-Xmx4000m

import sys
sys.path.append("../code/mod/")
from brain_io_wrapper import load_brain_from_file, save_brain_as_ofn

load_brain_from_file(sys.argv[1])

# Should probably switch to a dedicated AP.  Perhaps Query_menu_type ?  Or gross_category?  - Enforcing cardinality of 1.
def DL2subset(ont, DL_query, subset_tag):
    terms = ont.getSubClasses(DL_query, 0)
    for t in terms:
        ont.annotation(t, "inSubset", subset_tag)

# Load up ontology with relevant subproperties
o.learn("vfb_ext.owl") # local version. Should switch to URI
DL2subset(ont = o, DL_query = "BFO_0000050 some FBbt_00005093", subset_tag = "ns_part") # General tag for filtering autocomplete -> Nervous system.  Change to overlaps?
DL2subset(ont = o, DL_query = "FBbt_00040005", subset_tag = "synaptic_neuropil") # synaptic neuropil menus
DL2subset(ont = o, DL_query = "FBbt_00005099", subset_tag = "tract") # Tract menus
DL2subset(ont = o, DL_query = "FBbt_00007683", subset_tag = "clone") # Clone menus
DL2subset(ont = o, DL_query = "FBbt_00005106", subset_tag = "neuron") # neuron menus


save_brain_as_ofn(sys.argv[1])

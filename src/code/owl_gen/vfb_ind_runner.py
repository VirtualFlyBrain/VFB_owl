#!/usr/bin/env jython -J-Xmx8000m
import sys
sys.path.append('../mod')
sys.setrecursionlimit(2000)
from obo_tools import addOboAnnotationProperties, addVFBAnnotationProperties
#from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
#from com.ziclix.python.sql import zxJDBC
#from lmb_fc_tools import get_con
from vfb_ind_tools import gen_ind_by_source, add_facts, load_ont
from dict_cursor import dict_cursor
from neo4j_tools import neo4j_connect
import os

# Refactoring needed: Passing a dict of ontologies is pretty opaque. 
# Need to hard wire calls to corrects dicts into code
# Relying on keys => No scope control or checks for declaration, code completion etc.
# In its current form - doesn't allow passing of some key info such as baseURI. P
# DM could be extended to allow this, but this seems like more of the same crap. 
# Would an object-y model be better?  If so what struc?



"""ARG1: db username; ARG2: db password, ARG3: dataset name; 
ARG4(!) path to FBbt version used throughout - can be local path or full URL.
"""

# conn = get_con()
nc = neo4j_connect(sys.argv[1], sys.argv[2], sys.argv[3])

dataset = sys.argv[4]
FBBT = sys.argv[5]
# cursor = conn.cursor()
# Seem to have moved back to hard wiring this!
# cursor.execute("SELECT baseURI FROM ontology where short_name = 'vfb_ind'")
# dc = dict_cursor(cursor)
# baseURI = ''
# for d in dc:
# 	baseURI = d['baseURI']
# cursor.close()

# Setting by hand again for now (!).  Base URI not actually used in ind gen as full IRI taken from KB.
vfb_ind = Brain("http://virtualflybrain.org/reports/", "http://purl.obolibrary.org/obo/fbbt/vfb/" + dataset + ".owl") # This sets entity generation to use baseURI from DB. 
# vfb_ind = Brain(baseURI, baseURI + dataset + ".owl") # This sets entity generation to use baseURI from DB. 

vfb_image = Brain()  # Not specifying base as there seems to be a bug that overides full URL specified when adding individuals.  Not ideal!
addOboAnnotationProperties(vfb_ind)
#addOboAnnotationProperties(vfb_image)
addVFBAnnotationProperties(vfb_ind)
#vfb_image.addObjectProperty('http://xmlns.com/foaf/0.1/depicts')
#vfb_image.addClass('http://xmlns.com/foaf/0.1/image')


ont_dict = {}
ont_dict['fbbt'] = load_ont(FBBT)
#ont_dict['fbbt'] = load_ont("http://purl.obolibrary.org/obo/fbbt/%s/fbbt-simple.owl" % fbbt_release_version)
ont_dict['fb_feature'] = load_ont("../../owl/fb_features.owl")
#ont_dict['fb_feature'] = load_ont("http://purl.obolibrary.org/obo/fbbt/vfb/fb_features.owl")
ont_dict['vfb_ind'] = vfb_ind
#ont_dict['vfb_image'] = vfb_image  # Commenting for now as problems rolling some image files 
gen_ind_by_source(nc, ont_dict, dataset)
#add_facts(cursor=conn.cursor(), ont=vfb_ind, source=dataset) # Before turning this on, need to make sure all inds declared first.
vfb_ind.save("../../owl/" + dataset + ".owl")
#vfb_image.save("../../owl/" + dataset + "_image.owl")
vfb_ind.sleep()
ont_dict['fbbt'].sleep()
ont_dict['fb_feature'].sleep()


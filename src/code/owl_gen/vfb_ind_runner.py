#!/usr/bin/env jython -J-Xmx8000m
import sys
sys.path.append('../mod')
from obo_tools import addOboAnnotationProperties, addVFBAnnotationProperties
#from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
#from com.ziclix.python.sql import zxJDBC
from lmb_fc_tools import get_con
from vfb_ind_tools import gen_ind_by_source
from vfb_ind_tools import load_ont
from dict_cursor import dict_cursor
import os

# Refactoring needed: Passing a dict of ontologies is pretty opaque. 
# Need to hard wire calls to corrects dicts into code
# Relying on keys => No scope control or checks for declaration, code completion etc.
# In its current form - doesn't allow passing of some key info such as baseURI. P
# DM could be extended to allow this, but this seems like more of the same crap. 
# Would an object-y model be better?  If so what struc?



"""ARG1: db username; ARG2: db password, ARG3: dataset name; ARG4(!) path to FBBT
ARG4: local path to version of fbbt used throughout.
"""

conn = get_con(sys.argv[1], sys.argv[2])

#conn = zxJDBC.connect("jdbc:mysql://127.0.0.1:3307/flycircuit", sys.argv[1], sys.argv[2], "org.gjt.mm.mysql.Driver") # To be used via ssh tunnel.

dataset = sys.argv[3]
FBBT = sys.argv[4]
cursor = conn.cursor()
cursor.execute("SELECT baseURI FROM ontology where short_name = 'vfb_ind'")
dc = dict_cursor(cursor)
baseURI = ''
for d in dc:
	baseURI = d['baseURI']
cursor.close()

vfb_ind = Brain(baseURI, baseURI + dataset + ".owl")
vfb_image = Brain()  # Not specifying base as there seems to be a bug that overides full URL specified when adding individuals.  Not ideal!
addOboAnnotationProperties(vfb_ind)
addOboAnnotationProperties(vfb_image)
addVFBAnnotationProperties(vfb_ind)
vfb_image.addObjectProperty('http://xmlns.com/foaf/0.1/depicts')
vfb_image.addClass('http://xmlns.com/foaf/0.1/image')


ont_dict = {}
ont_dict['fbbt'] = load_ont(FBBT)
#ont_dict['fbbt'] = load_ont("http://purl.obolibrary.org/obo/fbbt/%s/fbbt-simple.owl" % fbbt_release_version)
ont_dict['fb_feature'] = load_ont("../../owl/fb_features.owl")
#ont_dict['fb_feature'] = load_ont("http://purl.obolibrary.org/obo/fbbt/vfb/fb_features.owl")
ont_dict['vfb_ind'] = vfb_ind
#ont_dict['vfb_image'] = vfb_image  # Commenting for now as problems rolling some image files 
gen_ind_by_source(conn.cursor(), ont_dict, dataset)
vfb_ind.save("../../owl/" + dataset + ".owl")
vfb_image.save("../../owl/" + dataset + "_image.owl")
conn.close()
vfb_ind.sleep()
ont_dict['fbbt'].sleep()
ont_dict['fb_feature'].sleep()


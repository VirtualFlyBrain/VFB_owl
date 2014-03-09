#!/usr/bin/env jython -J-Xmx8000m
import warnings
import sys
sys.path.append('../mod')
from obo_tools import addOboAnnotationProperties
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
from lmb_fc_tools import get_con
from vfb_ind_tools import gen_ind_by_source
from vfb_ind_tools import load_ont

conn = get_con(sys.argv[1], sys.argv[2])
dataset = sys.argv[3]
vfb_ind = Brain("http://www.virtualflybrain.org/", "http://purl.obolibrary.org/obo/fbbt/vfb/" + dataset + ".owl") # Should be set in DB?
addOboAnnotationProperties(vfb_ind)

ont_dict = {}
ont_dict['fbbt'] = load_ont("/repos/fbbtdv/fbbt/releases/fbbt-simple.owl")
#ont_dict['fbbt'] = load_ont("http://purl.obolibrary.org/obo/fbbt/%s/fbbt-simple.owl" % fbbt_release_version)
ont_dict['fb_feature'] = load_ont("../../owl/fb_features.owl")
#ont_dict['fb_feature'] = load_ont("http://purl.obolibrary.org/obo/fbbt/vfb/fb_features.owl")
ont_dict['vfb_ind'] = vfb_ind
gen_ind_by_source(conn.cursor(), ont_dict, dataset)
vfb_ind.save("../../owl/" + dataset + ".owl")
conn.close()
vfb_ind.sleep()
ont_dict['fbbt'].sleep()
ont_dict['fb_feature'].sleep()


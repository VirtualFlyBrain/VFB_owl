#!/usr/bin/env jython
import warnings
import sys
sys.path.append('../mod')
from obo_tools import addOboAnnotationProperties
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
from lmb_fc_tools import get_con
from vfb_ind_tools import gen_ind_by_source

conn = get_con(sys.argv[1], sys.argv[2])
dataset = sys.argv[3]
vfb_ind = Brain("http://www.virtualflybrain.org/owl/", "http://www.virtualflybrain.org/owl/" + dataset + ".owl")
addOboAnnotationProperties(vfb_ind)
gen_ind_by_source(conn.cursor(), vfb_ind, dataset)
vfb_ind.save("../../owl/" + dataset + ".owl")
conn.close()
vfb_ind.sleep()

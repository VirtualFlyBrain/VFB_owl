#!/usr/bin/env jython


from lmb_fc_tools import update_class_labels;
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
from lmb_fc_tools import get_con
import sys

con = get_con(sys.argv[1], sys.argv[2])

fbbt = Brain()
fbbt.learn("http://purl.obolibrary.org/obo/fbbt/fbbt-simple.owl")
update_class_labels('fbbt', fbbt, con)

so = Brain()
so.learn("http://purl.obolibrary.org/obo/so.owl")
update_class_labels('so', so, con)

fb = Brain()
fb.learn("file:///repos/VFB_owl/src/owl/fb_features.owl")
update_class_labels('fb_feat', fb, con)

ro = Brain()
ro.learn("http://purl.obolibrary.org/obo/ro.owl")
update_class_labels('ro', ro, con)

vfb = Brain()
vfb.learn("file:///repos/VFB_owl/src/owl/vfb_ext.owl")
update_class_labels('vfb_ext', vfb, con)

con.close()

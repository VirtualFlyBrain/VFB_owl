#!/usr/bin/env jython -J-Xmx3000m

import sys
from uk.ac.ebi.brain.core import Brain
sys.path.append('../mod')
from lmb_fc_tools import get_con, owlDbOnt
con = get_con(sys.argv[1], sys.argv[2])

obo = "http://purl.obolibrary.org/obo/"
vfb = obo + "fbbt/vfb/"

paths = [obo + "fbbt/fbbt-simple.owl",
         obo + "so.owl",
         vfb + "fb_features.owl",
         obo + "ro.owl",
         vfb + "vfb_ext.owl"
         ]

# Could be done with one big brain file in memory, but would require lots of ram to run
for p in paths:
    b = Brain()
    b.learn(p)
    od = owlDbOnt(con, b)
    od.update_labels()
    b.sleep()

con.close()

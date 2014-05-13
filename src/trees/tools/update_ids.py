#!/usr/bin/env jython -J-Xmx8000m
import json # Requires 2.7 !  Using beta1
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
from json_tree_tools import *
import re

### Think this now works, but note that domain colours will need to be chosen for each new domain.  Do we also have domain centres?
### Also - all of this should go into DB - in stack table (we'll need multiple stacks)

#### Doing this the OWL-ish way.

### individual - adult brain
### individuals for all domains - domain ID goes in external IDs? - Hmmm - really should be an external ID table with a column for the name of the external ID.
### All will be typed via regular type table.
### part_of/has_part relations - Needs FACT table.

### Note - this would be treating multiple paintings of the same brain as different individuals. Seems reasonable though.

fbbt = Brain()
fbbt.learn("http://purl.obolibrary.org/obo/fbbt/fbbt-simple.owl")

# This bit really should be a separate module - being file dependent.
oboid_domId = {}
JC = open("../json/JFRC_FBbt_correspondence.", "r")
for l in JC:
	l2 = l.rstrip()
	clist = l2.split("\t")
	if not re.search("_L$", clist[0]): 
		oboid_domId[clist[3]]=clist[2]

tc = load_json("../json/treeContent.jso")

new_tc = []
known_term_list = []

for term in tc:
	oboid = term["extId"][0]
	known_term_list.append(oboid)
	if oboid in oboid_domId:
		if "domainId" in term["domainData"]:
			term["domainData"]["domainId"] = oboid_domId[oboid] # Terns that didn't formerly have domainId will not, at the point
		else:
			term["domainData"] = {"domainColour": [0,128,128,127],"domainId": oboid_domId[oboid],"domainSelected": "false"} # Setting default colour - will need to fix.
	else:
		if "domainId" in term["domainData"]:
			term["domainData"]["domainId"] = '' # Remove old domain_id, if present.
		owl_id = re.sub(':','_',oboid)
		name = '';
		if fbbt.knowsClass(owl_id):
			name = fbbt.getLabel(owl_id)
		print "Ignoring %s %s as , according to the mapping file, it is not a painted domain." % (oboid, name)
	new_tc.append(term)

    
	# Adding records for any new terms
for oboid, domid in oboid_domId.items():
	if oboid not in known_term_list:
		new_tc.append({"domainData":{"domainColour": [0,128,128,127],"domainId": domid,"domainSelected": "false"}, "extId": [oboid],"nodeState": {"open": "false", "selected": "false"} }) # Anything generated here will need a new nodeId.

update_names(new_tc, fbbt)

fbbt.sleep()

write_json(new_tc, "../json/treeContent_JFRC_BN_final.jso")    


    
    
    

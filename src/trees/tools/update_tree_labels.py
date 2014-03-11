#!/usr/bin/env jython -J-Xmx8000m
import json # Requires 2.7 !  Using beta1
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
import re


# node1 = json_tree[0]
# shortFormID = node1['extId'][0]
# name = node1['name']

# ## Pretty print output

# json.dumps(node1,sort_keys=True, indent=4, separators=(',', ': '))


fbbt = Brain()
fbbt.learn("http://purl.obolibrary.org/obo/fbbt/fbbt-simple.owl")
treefile = open("../json/treeContent.jso", "r")
tree = treefile.read()
treefile.close()
json_tree = json.loads(tree)

# writing backup file using same ordering as output
backup = open("../json/treeContent_backup.jso", "w")
backup.write(json.dumps(json_tree ,sort_keys=True, indent=4, separators=(',', ': ')))
backup.close()

for node in json_tree:
	OBO_ID = node['extId'][0]
	shortFormID = re.sub(':', '_', OBO_ID)
	node['name'] = fbbt.getLabel(shortFormID)

fbbt.sleep()

treefile = open("../json/treeContent.jso", "w")
treefile.write(json.dumps(json_tree ,sort_keys=True, indent=4, separators=(',', ': ')))
treefile.close()

    
    
    


#!/usr/bin/env jython -J-Xmx8000m
import json # Requires 2.7 !  Using beta1
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
import json
import re

# DONE: Check relationship of tree node IDs to stack IDs.
# There is no relationship.  treeContent.jso stores links the node and stack (label field) IDs.  As far as I can tell, arbitrary assignment of node IDs is possible. They  seem to be in order in the tree, but it seems very unlikely that this is important.

# TODO - split out functions requiring Brain?

"""A set of functions for operating on the JSON files that define trees on VFB"""

def load_json(path):
    json_file = open(path, "r")
    json_string = json_file.read()
    json_file.close()
    return json.loads(json_string)

def write_json(json_var, path):
	"""Writes json_var to file (path) with a nicely serialised layout."""
	json_file = open(path, "w")
	json_file.write(json.dumps(json_var ,sort_keys=True, indent=4, separators=(',', ': ')))
	json_file.close()

def update_names(treeContent, fbbt):
	"""Updates names in treeContent (1st arg) using a Brain object (fbbt) as reference."""
	for node in treeContent:
		OBO_ID = node['extId'][0]
		shortFormID = re.sub(':', '_', OBO_ID)
		node['name'] = fbbt.getLabel(shortFormID)

def serialise_json_file(path):
	json_var = load_json(path)
	write_json(path)

def add_leaf(nodeId, tree, parent_nodeId):
	"""Adds a leaf node with specified nodeID (arg[0]) to a VFB  JSON treeStructure specified in arg[1] under parent with parent_nodeId specified in arg[2] """
	for v in tree.values():
		if (v['nodeId'] == parent_nodeId):
			if 'children' in v:
				v['children'].append({"node":{"nodeId": nodeId}})
			else:
				v['children'] = [{"node":{"nodeId": nodeId}}]
		else:
			if 'children' in v:
				for subtree in v['children']:
					add_leaf(nodeId, subtree, parent_nodeId) #is this sufficient exit condition?

def test_add_leaf():
	treeStructure = load_json("../json/treeStructure.jso")
	add_leaf("200", treeStructure, "77")
	write_json(treeStructure, "treeStructure_add_leaf_test.json")

# def add_treeContent():
	

def roll_readable_tree(id_name, tree, count=0):
	for v in tree.values():
		ID = v['nodeId']
		print count * '..' + id_name[ID]
		if 'children' in v:
			count += 1
			for subtree in v['children']:
				roll_readable_tree(id_name, subtree, count) #is this sufficient

        












    


#!/usr/bin/env jython -J-Xmx8000m
import json # Requires 2.7 !  Using beta1
#from uk.ac.ebi.brain.error import BrainException
#from uk.ac.ebi.brain.core import Brain
import re

# DONE: Check relationship of tree node IDs to stack IDs.
# There is no relationship.  treeContent.jso stores links the node and stack (label field) IDs.  As far as I can tell, arbitrary assignment of node IDs is possible. They  seem to be in order in the tree, but it seems very unlikely that this is important.

# TODO - split out functions requiring Brain?

# Potential major refactoring - use object orientation to abstract out tree crawling 
# from operations on/with tree content.  The challenge will be developing a system for 
# managing (arbitrary numbers of) additional arguments to be passed on tail recursion.

"""A set of functions for operating on the JSON files that define trees on VFB.
  Note that - after every tree structure manipulation it is essential to re-serialise 
  nodeId numbering and ordering in the treeStructure, treeContent file pair using the
  function update_node_IDs().  Without this, the javascript on VFB will barf on the files.
  """


# Tree structure for ref. 
#     "node": {
#         "nodeId": "18"
#     }
# },
# {
#     "node": {
#         "children": [
#             {
#                 "node": {
#                     "nodeId": "20"
#                 }
#             },
#             {
#                 "node": {
#                     "nodeId": "21"
#                 }
#             }
#         ],
#         "nodeId": "19"
#     }
# },

def load_json(path):
    json_file = open(path, "r")
    json_string = json_file.read()
    json_file.close()
    return json.loads(json_string)

def write_json(json_var, path):
    """Writes json_var to file (path) with a nicely serialised layout."""
    json_file = open(path, "w")
    json_file.write(json.dumps(json_var ,sort_keys=True, indent=4, separators=(',', ': '))) # Hmmm - sort keys here might prevent required ordering. - test.
    json_file.close()
    
def init_treeStructure():
    """Returns a treeStructure root"""
    return {
    "node": {
        "children": [ 
        ],
        "nodeId": "0"
    }
    }
    
def blank_treeContent_node(nodeId, name, oboID, domainId = '', color = [], centre = []):
    node = {
        "domainData": {
            "domainSelected": "false",
        },
        "extId": [
            oboID
        ],
        "name": name,
        "nodeId": nodeId,
        "nodeState": {
            "open": "true",
            "selected": "false"
        }
    }
    if domainId:
        node['domainData']['domainId'] = domainId
    if domainId:
        node['domainData']['domainColour'] = color
    if domainId:
        node['domainData']['domainCentre'] = centre
    
    return node

def update_names(treeContent, fbbt):
    """Updates names in treeContent (1st arg) using a Brain object (fbbt) as reference."""
    for node in treeContent:
        OBO_ID = node['extId'][0]
        shortFormID = re.sub(':', '_', OBO_ID)
        node['name'] = fbbt.getLabel(shortFormID)

def owl2Tree_init(treeContent, ont):
    d = {}
    tree_classes = []
    for node in treeContent:
        OBO_ID = node['extId'][0]
        shortFormID = re.sub(':', '_', OBO_ID)
        tree_classes.append(shortFormID)
    for shortFormID in tree_classes:
        all_subclasses = ont.getSubClasses(shortFormID)
        all_parts = ont.getSubClasses("BFO_0000050 some %s" % shortFormID)
        tree_parts = set(all_parts).intersection_update(set(tree_classes))
        tree_subclasses = set(all_subclasses).intersection_update(set(tree_classes))
        d['shortFormID'] = tree_subclasses.update(tree_parts)
    return d


        # Any node that contains whole tree apart from itself is root.
        # Any node that contains whole tree apart from itself and its parent is root for longest branch
        # So, could potentially iterate to build representation of longest branch.
        # Exit condition is hitting a leaf - a term with no children.
        # Then backtrack to build representation of next longest branch
        # etc until complete. Seems like a good case for recursion 
        # Data structure.  
        # Should be possible to build as for treeStructure, but with SFIDs for nodes ids
        # Then trivial to convert to using separate node Ids...
        
def fu(root, d, tree):
    for node in d['root']:
        subdict = d.pop('root')
        max_key = max(d, key= lambda x: len(d[x]))
        
        # find longest, or if multiple of same length, choose one randomly
        # add this sfid as a node under root
        # Then iterate through all terms in list under this node
        # Find longest...
        # keep going until hit a term with no children, subtracting each node you find from the list to iterate over
        # (Hmmm - is this a recipe for single inheritance?)
        # Then back track to children of root  and start from 2nd longest.


def update_centres(treeContent, domainId_centre):
    """Modified a treeContent JSON (1st arg) by substituting domain centres 
    specified in a dict (2nd arg) keyed on domainId"""
    for node in treeContent:
        if 'domainData' in node:
            if 'domainId' in node['domainData']:
                if node['domainData']['domainId']:
                    domId = node['domainData']['domainId']
                    node['domainData']['domainCentre']= domainId_centre[domId]

def serialise_json_file(path):
    json_var = load_json(path)
    write_json(path)

def blank_tree_node_no_dom():
    return {u'extId': [], u'nodeId': u'', u'nodeState': {u'open': u'false', u'selected': u'false'}, u'domainData': {u'domainSelected': u'false'}, u'name': u''}

def blank_tree_node_with_dom():
    return {u'extId': [], u'nodeId': u'', u'nodeState': {u'open': u'false', u'selected': u'false', u'domainColour': [], u'domainCentre': [], u'domainId': u''}, u'domainData': {u'domainSelected': u'false'}, u'name': u''}
    

def add_leaf(nodeId, tree, parent_nodeId):
    """Adds a leaf node with specified nodeID (arg[0]) to a VFB  
    JSON treeStructure specified in arg[1] under parent with 
    parent_nodeId specified in arg[2] """
    for v in tree.values():
        if (v['nodeId'] == parent_nodeId):
            if 'children' in v:
                v['children'].append({"node":{"nodeId": nodeId}}) # Append node to existing list of child nodes
            else:
                v['children'] = [{"node":{"nodeId": nodeId}}]  # Add new node as first child of spec parent
        else:
            if 'children' in v:
                for subtree in v['children']:
                    add_leaf(nodeId, subtree, parent_nodeId) #is this sufficient exit condition?

def add_leaf_by_name(treeContent, treeStructure, parent, child):
    name_nodeId = {}
    for node in treeContent:
        ID = node['nodeId']
        name = node['name']
        name_nodeId[name]=ID
    add_leaf(name_nodeId[child], treeStructure, name_nodeId[parent])

def find_and_return_subtree(nodeId, tree, subtree_out = '', address = []):
    """Returns a subtree starting from a specified node.  
    Should also return an address for that subtree that 
    could be used to specify it for deletion. But so far this does not work."""
    # The difficulty here is the snipping bit.  If I can get it to store an adress, then it will work with single inheritance.  Looks like this adress will need to be rolled as it goes.
    if not subtree_out:
        for k, v in tree.items():
            if (v['nodeId'] == nodeId):
                subtree_out = {}
                subtree_out['node'] = v
                address_out = address
                break
            #tree.pop(k)  #  Hmmmm - probably not be operating on tree passed at start of function.  Can store this = but then need full address to specify its deletion!
            elif 'children' in v:
                i = 0                
                for subtree in v['children']:
                    address.append(i)
                    i += 1
                    (subtree_out, address) = find_and_return_subtree(nodeId, subtree, subtree_out, address) # pass the return value(s) back up the stack.
    return (subtree_out, address)

# In order to specify for deletion, need to store array indexes!
    

def append_branch(nodeId, tree, new_subtree):
    for v in tree.values():
        if (v['nodeId'] == nodeId):
            if not 'children' in v:
                v['children'] = []
            print type(v['children'])
            v['children'].append(new_subtree)  # Add new node as first child of spec parent
            break
        elif 'children' in v:
            for subtree in v['children']:
                append_branch(nodeId, subtree, new_subtree)

                        
def copy_node(nodeId, tree, new_parent_id_node):
    # Unfinished code
    address = ''
    subtree = ''
    (subtree, address) = find_and_return_subtree(nodeId, tree)
    append_branch(new_parent_id_node, tree, subtree)


def test_add_leaf():
    treeStructure = load_json("../json/treeStructure.jso")
    add_leaf("200", treeStructure, "77")
    write_json(treeStructure, "treeStructure_add_leaf_test.json")

# def add_treeContent():

def roll_readable_tree(id_name, tree, count=0):
    for v in tree.values():
        ID = v['nodeId']
        print count * '..' + ID + ' ' + id_name[ID]
        if 'children' in v:
            count += 1
            for subtree in v['children']:
                roll_readable_tree(id_name, subtree, count)

def get_nodeId_oboid(treeContent):
    """Rolls a dict of nodeId to oboID Given a treeContent json"""
    nodeId_oboID = {}
    for node in treeContent:
        ID = node['nodeId']
        oboID = node['extId'][0]
        nodeId_oboID[ID]=oboID
    return nodeId_oboID

def get_nodeId_name(treeContent):
    """Rolls a dict of nodeId to oboID Given a treeContent json"""
    nodeId_name = {}
    for node in treeContent:
        ID = node['nodeId']
        nodeId_name[ID]=node['name']
    return nodeId_name

def roll_readable_tree_by_id(treeContent, treeStructure):
    nid_oid = get_nodeId_oboid(treeContent)
    roll_readable_tree(nid_oid, treeStructure)

def roll_readable_tree_by_name(treeContent, treeStructure):
    nodeId_name = get_nodeId_name(treeContent)
    roll_readable_tree(nodeId_name, treeStructure)

def treeStruc_order_rep(treeStructure, outfile):
    """Writes a list of nodeId\toboID to a file specified by outfile. 
    The order of the list corresponds to the order of nodes in the tree"""
    for v in treeStructure.values():
        ID = v['nodeId']
        outfile.write(ID + "\n")
        if 'children' in v:
            for subtree in v['children']:
                treeStruc_order_rep(subtree, outfile)

def update_node_IDs(treeContent, treeStructure):
    """ Order the treeContent array by the order of nodes in treeStructure. 
    This is needed because of the borderline insane javascript tree parser we run on VFB """
    # Make tmp file with list of nodes in treeStructure order.
    outfile = open("array.tmp", "w")
    treeStruc_order_rep(treeStructure, outfile)
    outfile.close()

    # roll dict of tree nodeId to node from treeContent file
    nodeId_treeContentNode = {}
    for node in treeContent:
        nodeId = node['nodeId']
        nodeId_treeContentNode[nodeId] = node


    treeOrderArray=open("array.tmp", "r")
    new_tc = []
    i = 0
    old_nodeId_new_nodeId = {}
    # Roll new treeContent file with nodes in same order as treeStructure, renumbered by array index.
    for line in treeOrderArray:
        nodeId = line.rstrip("\n")
        new_node = nodeId_treeContentNode[nodeId]
        new_node['nodeId'] = str(i)
        old_nodeId_new_nodeId[nodeId] = str(i)
        new_tc.append(new_node)
        i += 1
    # TODO -Add something here to delete tmp file.
    update_ts_nodeIds(treeStructure, old_nodeId_new_nodeId)
    return (new_tc)

# def get_old2new_nodeId(treeOrderArray):
#      """Takes array of node Ids in orde"""
#      i = 0
#      oldNodeId_new_Node_id = {}
#      for line in treeOrderArray:
#          nodeId=line.rstrip("\n")
#          oldNodeId_new_Node_id[i]=nodeId # do these need to be strings?
#          i += 1
#      return oldNodeId_new_Node_id

def update_ts_nodeIds(treeStructure, oldNodeId_new_Node_id):
    for v in treeStructure.values():
        old_ID = v['nodeId']
        v['nodeId'] = oldNodeId_new_Node_id[old_ID]
        if 'children' in v:
            for subtree in v['children']:
                update_ts_nodeIds(subtree, oldNodeId_new_Node_id)

# def update_node_ids(treeContent, treeStructure):
#      outfile = open("array.tmp", "w")
#      treeStruc_order_rep(treeStructure, outfile)
#      outfile.close()
#      treeOrderArray=open("array.tmp", "r")
#      oldNodeId_new_Node_id = get_old2new_nodeId(treeOrderArray)
#      update_ts_nodeIds(treeStructure, oldNodeId_new_Node_id)
#      update_tc_nodeIds(treeContent, oldNodeId_new_Node_id)
#      treeOrderArray.close()


    
    
    
    
    
        
    

    

#!/usr/bin/env python

def tsv2pdm(tsv_file_path):
    """Makes a Python data model from as tsv file. The first line is treated as a header. The rest of the table becomes an array of dicts, keyed on the header. (This data model follows the same pattern as dict_cursor making switching between a DB representation and simple TSVs easy as long as TSV headers follow the same pattern as DB column headers.""" 
    tsv_file_obj = open(tsv_file_path, "r")
    hstat = 0
    headers = []
    tab = []
    for line in tsv_file_obj:
        cline = line.rstrip("\n")
        row = {}
        if hstat == 0:
            headers = cline.split("\t")
            hstat = 1
        else:
            content = cline.split("\t")
            i = 0
            for head in headers:
                row[head]=content[i]
                i += 1
            tab.append(row)
    tsv_file_obj.close()
    return tab

def dictList2row_column_cell(tab_dictList, key_row):
    """Turns a list of table represented as a list of dicts into a dict of dicts keyed on the contents of a specified key row."""
    row_column_cell = {}
    
    for d in tab_dictList:
        row_key = d[key_row]
        for column_key in d:
            if row_key not in row_column_cell:
                row_column_cell[row_key] = {}
            row_column_cell[row_key][column_key] = d[column_key]
    return row_column_cell

def blank_tree_node_with_dom():
	return {u'extId': [], u'nodeId': u'', u'nodeState': {u'open': u'false', u'selected': u'false'}, u'domainData': {u'domainSelected': u'false', u'domainColour': [], u'domainCentre': [], u'domainId': u''}, u'name': u''}


def nodeIdList(treeContent):
    """Returns a list of nodeIds as integers from a treeContent JSON"""
    list = []
    for node in treeContent:
        list.append(int(node['nodeId']))
    return list
        
def populate_node(node, row_dict):
    if not node['extId']:
        node['extId'].append(row_dict['oboId'])
    node['name'] = row_dict['name']
    node['domainData']['domainId']=row_dict['domainId']
    color = row_dict['domainColour'].split(",")
    node['domainData']['domainColour'].extend(color)
    centre = row_dict['domainCentre'].split(",")
    node['domainData']['domainCentre'].extend(centre)

def update_tree_jsons_from_tab(tab, treeContent, treeStructure):
    # Starting point is:
    ## 1. a table of domainIDs and mappings to FBbt + (potentially) domain centres and colours.
    ## 2. a treeContent file which needs new domain IDs for the domains it has (idenitfied by FBbt), + new domains added (Identified by there being no domain with this FBbt in the existing json file).
    # Make lookup list of FBbt in tree
    oboId_in_tc = []
    for node in treeContent:
         oboId_in_tc.append(node['extId'][0])
    # Roll lookup dict of tab row by FBbt.
    oboId_column_cell =  dictList2row_column_cell(tab, 'oboId')
    oboId_in_tab = oboId_column_cell.keys() 
    toReplace = set(oboId_in_tab) & set(oboId_in_tc)
    toAdd = set(oboId_in_tab) - set(oboId_in_tc)

    # Update existing nodes
    for node in treeContent:
        if node['extId'][0] in toReplace:
            populate_node(node, oboId_column_cell[node['extId'][0]])

    nodeIds = nodeIdList(treeContent)
    nodeId = 0 # Making nodeId integer to so it can be incremented.  Convert to string to use.
    # add new nodes
    for oboId in toAdd:
        node =  blank_tree_node_with_dom()
        populate_node(node, oboId_column_cell[oboId])
        # generate new nodeId
        while nodeId in nodeIds:
            nodeId +=1
        nodeIds.append(nodeId)
        node['nodeId'] = str(nodeId)
        treeStructure['node']['children'].append({ 'node': {'nodeId': str(nodeId)}})
        treeContent.append(node)        


    

                
        
    

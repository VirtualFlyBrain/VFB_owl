from tsv2pdm import tab
from json_tree_tools import blank_treeContent_node, write_json, add_leaf, load_json, roll_readable_tree, get_nodeId_name
import operator

#  Assume existing, valid domain tree files
#  Add two new nodes - one for tracts and one for neuropils?  - But do we have a terms?  
#  Definitely not for neuropils...  

# Or could try interleaving node. 
# TO do this, need a list of subnodes  # 

# Or just bung them on the end...

dts = load_json("../BrainName_domains/json/treeStructure.jso")
dtc = load_json("../BrainName_domains/json/treeContent.jso")
ttc_tab = tab("../BrainName_tracts/", "domain_data.tsv")

dlist = []
for d in dtc:
    if 'extId' in d.keys():
        if len(d['extId']) > 0:
            dlist.append(d['extId'][0])

# sort table on name field (ultimately) => alphabetic ordering of tree
ttc_tab.tab.sort(key=operator.itemgetter('name'))

D_nodeIds = []
for n in dtc:
    D_nodeIds.append(int(n['nodeId']))  
i = max(D_nodeIds) + 1


for r in ttc_tab.tab:
    # if domain is mapped
    if r['oboId']:
        # if not already in tree - append to end
        if r['oboId'] not in dlist:
            n = blank_treeContent_node(domainId=r['domainID'], nodeId=str(i), name = r['name'], oboID = r['oboId'], 
                                       color = r['domainColour'], centre = r['domainCentre'])
            dtc.append(n)
            add_leaf(str(i), dts, '0')
            i += 1
        
idn = get_nodeId_name(dtc)
roll_readable_tree(idn, dts)

write_json(json_var = dtc, path = "json/treeContent.jso")
write_json(json_var = dts, path = "json/treeStructure.jso")

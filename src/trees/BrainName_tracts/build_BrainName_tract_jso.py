from tsv2pdm import tab
from json_tree_tools import blank_treeContent_node, write_json, add_leaf, init_treeStructure
import operator
from __builtin__ import str

# Aim = single root: adult brain.  With an alphanumeric list of tracts underneath

tc_tab = tab("./", "domain_data.tsv")

# sort table on name field (ultimately) => alphabetic ordering of tree
tc_tab.tab.sort(key=operator.itemgetter('name'))

tc = []
i = 1

ts = init_treeStructure()

adult_brain_node = blank_treeContent_node(nodeId='0', name = 'adult brain', oboID = 'FBbt:00003624')
tc.append(adult_brain_node)

for r in tc_tab.tab:
    if r['oboId']:
        n = blank_treeContent_node(domainId=r['domainID'], nodeId=str(i), name = r['name'], oboID = r['oboId'], 
                           color = r['domainColour'], centre = r['domainCentre'])
        tc.append(n)
        add_leaf(str(i), ts, '0')
        i += 1


write_json(json_var = tc, path = "json/treeContent.jso")
write_json(json_var = ts, path = "json/treeStructure.jso")
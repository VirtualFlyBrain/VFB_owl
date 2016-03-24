from owl2pdm_tools import ont_manager
from uk.ac.ebi.brain.core import Brain
from neo4j_tools import neo4j_connect
import sys
import re

"""Add typing via anonymous class expressions from OWL file.
Requires uniqueness constraint on individual & class short_form_id."""

nc = neo4j_connect(base_uri = sys.argv[1], usr = sys.argv[2], pwd = sys.argv[3])
vom = ont_manager(file_path=sys.argv[4])


# vom.typeAxioms2pdm(sfid = 'VFB_00005000')
# example = [{'isAnonymous': False, 'objectId': u'FBbt_00100247'},
#            {'relId': u'BFO_0000050', 'isAnonymous': True, 'objectId': u'FBbt_00003624'},
#            {'relId': u'BFO_0000050', 'isAnonymous': True, 'objectId': u'FBbt_00007011'},
#            {'relId': u'RO_0002292', 'isAnonymous': True, 'objectId': u'FBtp0014830'}]

# Simple to use. Only issue is resolution of short_form_ids.  This can be done as long as these are stored as attributes on relations.  These should be added in the process of adding named relations.  Check proposed schema on ticket...


# Grabbing individuals from from neo4J, avoiding Brain.  Setting to VFB only for now.
statements = ["MATCH (i:VFB:Individual) RETURN i"]
r = nc.commit_list(statements)
inds = [x['row'][0]['short_form'] for x in r[0]['data']]


# Iterate over individuals, looking up types and adding them
statements = []
for i in inds:
    types = vom.typeAxioms2pdm(sfid = i)
    for t in types:
        if t['isAnonymous']:
            rel = re.sub(' ', '_', vom.get_labels(t['relId'])[0])
            # Using related link. Can denormalise with generic edge naming script.
            s = "MATCH (I:Individual), (C:Class) WHERE I.short_form = '%s'" \
                "AND C.short_form = '%s' MERGE (I)-[r:Related {label: '%s', short_form: '%s' }]->(C)" \
                % (i, t['objectId'], rel, t['relId']) # 
            statements.append(s)
    facts = vom.get_triples(sfid = i)
    for f in facts:
        rel = re.sub(' ', '_', vom.get_labels(vom.get_labels(f[1][0])))
        s = "MATCH (I1:Individual), (I2:Individual) " \
            "WHERE I1.short_form = '%s' and I1.short_form = '%s' " \
            "MERGE (I1)-[r:Related { label: '%s', short_form: '%s' }]-(I2)" \
            % (f[0], f[2], rel, f[1])
        statements.append(s)

nc.commit_list_in_chunks(statements, verbose = True, chunk_length = 1000)
#vfb.sleep()

# Inds from graph (probably don't need this)
# payload = {'statements': [{'statement': 'MATCH (i:Individual) RETURN i.short_form'}]}
# ind_q_res = requests.post(url = "%s/db/data/transaction/commit" % base_uri, auth = (usr, pwd) , data = json.dumps(payload))
# rj= rels.json()
# inds = rj['results'][0]['data']











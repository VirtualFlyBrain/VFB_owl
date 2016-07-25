from owltools.graph import OWLGraphWrapper
from owl2pdm_tools import ont_manager
from uk.ac.ebi.brain.core import Brain  # May be better to avoid Brain in this case...
import sys
import re
from neo4j_tools import neo4j_connect

"""Add typing via anonymous class expressions from OWL file.
Requires uniqueness constraint on individual & class short_form_id.
Sets uniqueness constraint on FBrf for all PUB."""

# Need to consider whether to use a unique id on pubs that is separate from FBrf.  This deals with the odd cases where we don't have an FBrf.

# Note: should be straightforward to remove dependency on Brain.  
# One option is to use Neo4J for the initial query.

batch = True
if len(sys.argv) == 6:
    arg = sys.argv.pop(1)
    if arg == '--no_batch':
        batch = False
    else:
        warnings.warn('Illegal argument %s' % arg)

nc = neo4j_connect(base_uri = sys.argv[1], usr = sys.argv[2], pwd = sys.argv[3])
ontology_uri = sys.argv[4]

supported_xrefs = { 'FlyBase' : 'FlyBase:FBrf\d{7}', 'PMID': 'PMID:\d+', 'DOI': 'DOI:.+', 'http' : 'http:.+'}


def proc_xrefs(dbxrefs):
    if not dbxrefs:
        return False
    out = {}
    for db in supported_xrefs.keys():
        out[db] = []
    for xref in dbxrefs:
        for db, re_string in supported_xrefs.items():
            m = re.compile(re_string)
            if re.match(m, xref):
                ref = xref.split(':')[1]
                out[db].append(ref)     
    return out

vfb = Brain()
vfb.learn(ontology_uri)
vom = ont_manager(vfb.getOntology())
ogw = OWLGraphWrapper(vfb.getOntology())


fbbt_classes = vfb.getSubClasses("FBbt_10000000", 0) # FBbt root
# To get the same list from neo4J:
# MATCH (a:Class)<-[:SUBCLASSOF*]-(b:Class) WHERE a.short_form = 'FBbt_10000000'  RETURN b.short_form

# Requires uniqueness constraint on pub key fields from start

# Add unattribued pub node and set uniqueness:
# (Separate commits needed as can't combined adding data with schema change.)
# By convention, unnattributed is a FlyBase attribute.  May want to change this.

statements = ["MERGE (:pub:Individual { FlyBase: 'Unattributed' })"]
nc.commit_list(statements)

for db in supported_xrefs:
    statements.append("CREATE CONSTRAINT ON (p:pub) ASSERT p.%s IS UNIQUE" % db)

nc.commit_list(statements)

def roll_cypher_add_def_pub_link(sfid, pub_id_typ, pub_id):
    """Generates a Cypher statement that links an existing class 
    to a pub node with the specified attribute.  Generates a new pub node
     if none exists."""
    return  "MATCH (a:Class { short_form : '%s' }) " \
            "MERGE (p:pub:Individual { %s : '%s' }) " \
            "MERGE (a)-[:has_reference { typ : 'def' }]->(p)"  % (sfid, pub_id_typ, pub_id)
            

def roll_cypher_add_syn_pub_link(sfid, s, pub_id_typ, pub_id):
    """Generates a Cypher statement that links an existing class 
    to a pub node ..."""  
    label = re.sub("'", "\'", s.getLabel())
    return  "MATCH (a:Class { short_form : '%s' }) " \
            "MERGE (p:pub:Individual { %s : '%s' }) " \
            "MERGE (a)-[:has_reference { typ : 'syn', scope: '%s', synonym : \"%s\", cat: '%s' }]->(p)" \
            "" % (sfid, pub_id_typ, pub_id, s.getScope(), label, s.getCategory())


statements = []

for sfid in fbbt_classes:
    dbxrefs = ogw.getDefXref(vom.bi_sfp.getEntity(sfid))
    pub_refs = proc_xrefs(dbxrefs)
    syns = ogw.getOBOSynonyms(vom.bi_sfp.getEntity(sfid))
    if pub_refs:
        for db in supported_xrefs.keys():
            for ref in pub_refs[db]:
                statements.append(roll_cypher_add_def_pub_link(sfid, pub_id_typ = db, pub_id = ref))

    if syns:
        for s in syns:
            pub_refs = proc_xrefs(s.getXrefs())
            if pub_refs:
                for db in supported_xrefs.keys():
                    for ref in pub_refs[db]:
                        statements.append(roll_cypher_add_syn_pub_link(sfid, s, pub_id_typ = db, pub_id = ref))         
            else:
                statements.append(roll_cypher_add_syn_pub_link(sfid, s, pub_id_typ = 'FlyBase', pub_id = 'Unattributed'))           

if batch: 
    chunk_length = 500
else:
    chunk_length = 1
    
nc.commit_list_in_chunks(statements, verbose= True, chunk_length = chunk_length)

vfb.sleep()
        





        
        

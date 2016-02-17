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

nc= neo4j_connect(base_uri = sys.argv[1], usr = sys.argv[2], pwd = sys.argv[3])
ontology_uri = sys.argv[4]


def proc_xrefs(dbxrefs):
    out = []
    if not dbxrefs:
        return out
    else:
        for xref in dbxrefs:
            if re.match("FlyBase:FBrf\d{7}", xref):
                fbrf = xref.split(':')[1]
                out.append(fbrf)
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

statements = ["MERGE (:pub:Individual { FlyBase: 'Unattributed' })"]
nc.commit_list(statements)
statements = ["CREATE CONSTRAINT ON (p:pub) ASSERT p.FlyBase IS UNIQUE"]
nc.commit_list(statements)


statements = []

for sfid in fbbt_classes:
    dbxrefs = ogw.getDefXref(vom.bi_sfp.getEntity(sfid))
    fbrfs = proc_xrefs(dbxrefs)
    syns = ogw.getOBOSynonyms(vom.bi_sfp.getEntity(sfid))
    if fbrfs:
        for fbrf in fbrfs:
            statements.append("MATCH (a:Class { short_form : '%s' }) " \
                              "MERGE (p:pub:Individual { FlyBase : '%s' }) " \
                              "MERGE (a)-[:has_reference { typ : 'def' }]->(p)"
                               % (sfid, fbrf))
    if syns:
        for s in syns:
            fbrfs = proc_xrefs(s.getXrefs())
            label = re.sub("'", "\'", s.getLabel())
            if fbrfs: 
                for f in fbrfs:
                    statements.append("MATCH (a:Class { short_form : '%s' }) " \
                                      "MERGE (p:pub:Individual { FlyBase : '%s' }) " \
                                      "MERGE (a)-[:has_reference { typ : 'syn', scope: '%s', synonym : \"%s\", cat: '%s' }]->(p)"
                                      % (sfid, f, s.getScope(),label, s.getCategory()))
            else:
                statements.append("MATCH (a:Class { short_form : '%s' }) " \
                                      "MERGE (p:pub:Individual { FlyBase : '%s' }) " \
                                      "MERGE (a)-[:has_reference { typ : 'syn', scope: '%s', synonym : \"%s\", cat: '%s' }]->(p)"
                                      % (sfid, 'Unattributed', s.getScope(), label, s.getCategory()))
        
nc.commit_list_in_chunks(statements, verbose= True, chunk_length = 500)

vfb.sleep()
        





        
        

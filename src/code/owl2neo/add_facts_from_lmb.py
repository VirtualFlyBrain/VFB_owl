# A temporary expedient until import from OWL fixed, or we move to a native neo4J implementation of KB

from neo4j_tools import neo4j_connect
from lmb_fc_tools import get_con, dict_cursor
from com.ziclix.python.sql import zxJDBC # FOR DB connection  # Better to switch to OBDC but having probs with iOS
import sys

# Requires ssh tunnel

### Might be better to run from 


nc = neo4j_connect(base_uri = sys.argv[1], usr = sys.argv[2], pwd = sys.argv[3])
c = get_con(sys.argv[4], sys.argv[4])
cursor = c.cursor()

# TBA: Make sure uniqueness constraints in place!

cursor.execute("SELECT s.shortFormID AS subj_sfid, " \
               "s.label AS subj_label,  " \
               "r.shortFormID AS rel_sfid,  " \
               "r.label as rel_label,  " \
               "o.shortFormID AS obj_sfid,  " \
               "o.label AS obj_label,  " \
               "ront.baseURI AS rBase,  " \
               "ront.short_name as ront_name  " \
               "FROM owl_fact f  " \
               "JOIN owl_individual s ON (f.subject=s.id)  " \
               "JOIN owl_individual o ON (f.object=o.id)  " \
               "JOIN owl_objectProperty r ON (f.relation = r.id)  " \
               "JOIN ontology ront ON (r.ontology_id=ront.id)  ")  # Just bare triples.  Not pulling types. 

cypher_facts = []

## Warning - hard wiring base URI here!
vfb_ind_base_uri = 'http://www.virtualflybrain.org/owl/'

# Failure on 'depicts' ?

for d in dict_cursor(cursor):
    # some relations (e.g. depicts) have no label
    if d['rel_label']:
        rel_label_string = ", label: '%s'" %  d['rel_label']
    else:
        rel_label_string = ''
    # First create individuals if the don't already exist.  Then create triple.    
    cypher_facts.append('MERGE (s:Individual:VFB { short_form : "%s", label : "%s" , ontology_name : "vfb", iri: "%s%s"}) ' \
                        'MERGE (s:Individual:VFB { short_form : "%s", label : "%s" , ontology_name : "vfb", iri: "%s%s"}) ' \
                        'MERGE (s)-[:Related { short_form : "%s" %s, iri : "%s%s" }]->(o)'\
                        % (d['subj_sfid'], d['subj_label'], vfb_ind_base_uri, d['subj_sfid'], 
                           d['obj_sfid'], d['obj_label'], vfb_ind_base_uri, d['obj_sfid'], 
                           d['rel_sfid'], rel_label_string, d['rBase'], d['rel_sfid']))
    
nc.commit_list_in_chunks(statements = cypher_facts, verbose = True, chunk_length = 10000) 

# Add type assertions for images inds from lmb:

cypher_image_types = []

cursor.execute("SELECT oc.shortFormID AS claz, " \
               "oi.shortFormID AS ind, " \
               "oop.shortFormID AS rel_sfid, " \
               "oop.label AS rel_label, " \
               "ront.baseURI AS rBase, " \
               "ront.short_name AS ront_name " \
               "FROM owl_individual oi " \
               "JOIN individual_type it ON oi.id=it.individual_id " \
               "JOIN owl_type ot ON it.type_id=ot.id " \
               "JOIN owl_class oc ON ot.class = oc.id " \
               "JOIN owl_objectProperty oop ON ot.objectProperty=oop.id " \
               "JOIN ontology ront ON (oop.ontology_id=ront.id) " \
               "WHERE (oi.shortFormID like 'VFBi%' OR oi.shortFormID like 'VFBc%')")


               
for d in dict_cursor(cursor):
    if not d['rel_sfid']:
        edge = ':INSTANCEOF'
    else:
        edge = ":Related { short_form : '%s', label : '%s', uri : '%s%s' }" \
                % (d['rel_sfid'], d['rel_label'], d['rBase'], d['rel_sfid'])
                
    cypher_image_types.append("MATCH (c:Class { short_form: '%s' }), (i:Individual:VFB { short_form : '%s' }) " \
                              "MERGE (i)-[%s]->(c)" % 
                              (d['claz'], d['ind'], edge))
    
nc.commit_list_in_chunks(statements = cypher_image_types, verbose = True, chunk_length = 10000)






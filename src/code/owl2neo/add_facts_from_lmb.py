# A temporary expedient until import from OWL fixed, or we move to a native neo4J implementation of KB

from neo4j_tools import neo4j_connect
from lmb_fc_tools import get_con, dict_cursor
from com.ziclix.python.sql import zxJDBC # FOR DB connection  # Better to switch to OBDC but having probs with iOS
import sys

# Requires ssh tunnel

### Might be better to run from 


nc = neo4j_connect(base_uri = sys.argv[1], usr = sys.argv[2], pwd = sys.argv[3])
c = get_con(sys.argv[4])
cursor = c.cursor()

cursor.execute("SELECT s.shortFormID as subj_sfid, " \
               "r.shortFormID as rel_sfid, label as rel_label, "\
               "o.shortFormID as obj_sfid FROM owl_fact f " \
               "JOIN owl_individual s ON (f.subject=s.id) " \
               "JOIN owl_individual o ON (f.object=o.id) " \
               "JOIN owl_objectProperty r ON (f.relation = r.id)")  # Just bare triples.  Not pulling types.  # But should!

cypher_facts = []

for d in dict_cursor(cursor):
    cypher_facts.append("MERGE (:Individual { short_form : '%s', label : '%s' })" \
                       "-[:RELATED { short_form : '%s', label : '%s' }]->(:Individual: { short_form : '%s', label : '%s' })" % 
                       (d['subj_sfid'], d['subj_label'], d['rel_sfid'], d['rel_label'] , d['obj_sfid'], d['obj_label']))
  
nc.commit_list_in_chunks(statements = cypher_facts, verbose = True, chunk_length = 1000)





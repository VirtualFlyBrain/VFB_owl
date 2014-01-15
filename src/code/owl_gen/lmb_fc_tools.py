#!/usr/bin/env jython

from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain

def oe_check_db_and_add(sfid, typ, cursor, ont):
    """Takes, sfid, owl type, cursor and ontology as Brain object as args. 
    Checks whether the sfid exists in the lmb owl_entity table, finds the appropriate base URI and then adds. 
    Returns true if the entity is in the table, flase if not"""

    cursor.execute("SELECT o.baseURI bu FROM ontology o JOIN owl_entity oe ON (oe.ontology=o.ontology_id) WHERE sfid = '%s'" % sfid)
	dc = dict_cursor(cursor)
	bu = ''
	for d in dc:
		bu = d['bu']
	if bu:
		ont.addClass(bu+sfid)
		return 1
	else
		return 0
    
def BrainName_mapping(cursor, ont):
    cursor.execute("SELECT b2o.BrainName_abbv, oe.shortFormID FROM BrainName_to_owl b2o JOIN owl_entity oe ON (oe.id=b2o.owl_entity_id)")
    BN_dict = {}
    dc = dict_cursor(cursor)
    for d in dc:
        BN = d["BrainName_abbv"]
        owl_class = d["shortFormID"]
        BN_dict[BN] = owl_class
        if not vfb_ind.knowsClass(owl_class): 
            oe_check_db_and_add(owl_class, 'class', cursor, ont)
    return BN_dict
    
    

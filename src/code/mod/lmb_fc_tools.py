#!/usr/bin/env jython

from com.ziclix.python.sql import zxJDBC # FOR DB connection
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
from obo_tools import gen_id
import warnings

def get_con(usr, pwd):
	conn = zxJDBC.connect("jdbc:mysql://localhost/flycircuit",usr, pwd, "org.gjt.mm.mysql.Driver") # Use for local installation
	#conn = zxJDBC.connect("jdbc:mysql://127.0.0.1:3307/flycircuit", usr, pwd, "org.gjt.mm.mysql.Driver") # To be used via ssh tunnel.
	return conn

def update_class_labels(ont_name, ont, conn): # With a method to query ont name from ont, should be able to limit to 2 args
	"""Updates class labels in DB (connection via conn), using corresponding labels in ontology (brain object ont) applied to ontology corresponding to specified using file_name."""
	cursor1 = conn.cursor()
	cursor2 = conn.cursor()
	cursor1.execute("SELECT oc.shortFormID, oc.label FROM owl_class oc JOIN ontology o ON (oc.ontology_id=o.id) WHERE file_name = '%s'" % ont_name)
	dc = dict_cursor(cursor1)
	for d in dc:
		if ont.knowsClass(d['shortFormID']):
			new_label = ont.getLabel(d['shortFormID'])
			if not new_label == d['label']:
				update = "UPDATE owl_class set label='%s' WHERE shortFormID = '%s'" % (new_label, d['shortFormID'])
				#print update
				cursor2.execute(update)
				#print cursor2.warnings
		else:
			warn.warnings("Unknown class " +  d['shortFormID'])
	conn.commit() # without this - no updates actually get actioned!
	cursor1.close()
	cursor2.close()

def update_class_labels_test(usr,pwd,file,fname):
	conn = get_con(usr, pwd)
	ont = Brain()
	ont.learn(file)
	update_class_labels(fname, ont, conn)

def oe_check_db_and_add(sfid, typ, cursor, ont):
	"""Takes, sfid, owl type, cursor and ontology as Brain object as args. Checks whether the sfid exists in the lmb owl_entity table, finds the appropriate base URI and then adds to ont. Returns true if the entity is in the table, flase if not."""
	cursor.execute("SELECT o.baseURI bu FROM ontology o JOIN owl_entity oe ON (oe.ontology=o.ontology_id) WHERE shortFormID = '%s'" % sfid)
	dc = dict_cursor(cursor)
	baseURI = '' # As well as storing baseURI, serves as indicator.  Hmmm - probably not a good idea.  
	for d in dc:
		baseURI = d['bu'] # uniqueness constraint on table means there can be only 1  
	if baseURI:
		if typ == 'class':
			ont.addClass(baseURI+sfid)
		elif typ == 'objectProperty':
			ont.addObjectProperty(baseURI+sfid)
	else:
		warnings.warn("Unknown " + typ  + " " + sfid)
    
def BrainName_mapping(cursor, ont):
    cursor.execute("SELECT b2o.BrainName_abbv, oe.shortFormID FROM BrainName_to_owl b2o JOIN owl_entity oe ON (oe.id=b2o.owl_entity_id)")
    BN_dict = {}
    dc = dict_cursor(cursor)
    for d in dc:
        BN = d["BrainName_abbv"]
        owl_class = d["shortFormID"]
        BN_dict[BN] = owl_class
        if not ont.knowsClass(owl_class): 
            oe_check_db_and_add(owl_class, 'class', cursor, ont) # bit silly to check again when they come from the same DB!.
    return BN_dict

def gen_ind_dict(cursor):
	"""Generates a name:id dict of all individuals"""
	cursor.execute("SELECT shortFormID, label FROM owl_individual")
	dc = dict_cursor(cursor)
	id_name = {}
	for d in dc:
		id_name[d['shortFormID']] = d['label']
	return id_name

def add_ind(conn, ID, name, typ, source, id_name):
	cursor = conn.cursor()
 	(vfbid, ID) = gen_id('VFB', ID, 8, id_name)
 	id_name[vfbid] = name
 	cursor.execute("INSERT INTO owl_individual (shortFormID, uuid, label, type_for_def, source_id) VALUES ('%s', UUID(), '%s', '%s', (SELECT id as source_id from data_source where name = '%s'))" % (vfbid, name, typ, source))
	conn.commit()
	cursor.close()
 	return (vfbid, id_name, ID)
	
def make_ind_obsolete(conn, vfbid):
	cursor = conn.cursor()
 	cursor.execute("UPDATE owl_individual SET is_obsolete IS TRUE WHERE shortFormID = '%s'" % vfbid)
	conn.execute()
	cursor.close()

def add_ind_test(conn):
	cursor = conn.cursor()
	id_name = gen_ind_dict(cursor)
 	(vfbid, id_name, ID) = add_ind(conn, 16000, "add_ind_test", 'neuron', 'CostaJefferis', id_name)
 	cursor.execute("SELECT * from owl_individual WHERE label = 'add_ind_test'")
 	dc = dict_cursor(cursor)
 	for d in dc:
 		if d['label'] == "add_ind_test": 
 			return True
 	cursor.execute("DELETE from owl_individual WHERE label = 'add_ind_test'")
	conn.commit()
	cursor.close()
	

# def add_type_exp(cursor, objectProperty, claz):
# 	"""Add type exp to VFB DB"""

# def add_type_exp_by_label(cursor, objectProperty, claz):
#     op_id = ''
# 	cursor.execute("SELECT id from owl_entity where label = '%s' AND type = 'objectProperty'" % objectProperty)
# 	dc = dict_cursor(cursor)
# 	for d in dc:
# 		op = d['id']
# 	claz_id = ''
# 	cursor.execute("SELECT id from owl_entity where label = '%s' AND type = 'class'" % objectProperty)
# 	dc = dict_cursor(cursor)
# 	for d in dc:
# 		claz_id = d['id']
        

# def type_ind(cursor, objectProperty, claz):
# 	"""Add type to individual in LMB FC DB"""
    


	
	
	
	
	
    

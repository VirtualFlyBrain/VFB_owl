#!/usr/bin/env jython

from com.ziclix.python.sql import zxJDBC # FOR DB connection
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
#from uk.ac.ebi.brain.error import BrainException
#from uk.ac.ebi.brain.core import Brain
from obo_tools import gen_id
from owltools.graph import OWLGraphWrapper
import re
import warnings
#from fc_ind import ont_dict

# A big bag of functions for working with lmb fc mysql DB.

#Some refactoring to a more objecty approach could reduce number and complexity of args needed.
## But this refactoring should be limited to functions not being used in production of individuals.

## TODO: wrap compound key hack allowing for NULL in function.

def esc_quote(s):
	return re.sub("\'", "\\'", s)

def get_con(usr, pwd):
	#conn = zxJDBC.connect("jdbc:mysql://localhost/flycircuit",usr, pwd, "org.gjt.mm.mysql.Driver") # Use for local installation
	conn = zxJDBC.connect("jdbc:mysql://127.0.0.1:3307/flycircuit", usr, pwd, "org.gjt.mm.mysql.Driver") # To be used via ssh tunnel.
	return conn


class owlDbOnt():
	def __init__(self, conn, ont):
		"""Conn is a zxJBDC database handle;
		ont is a Brain Object"""
		self.conn = conn
		self.ont = ont
		self.onto = ont.getOntology()
		self.ogw = OWLGraphWrapper(self.onto)
		self.update_class_labels()
		
	def __str__(self):
		return str(self.conn)

	def update_class_labels(self): 
		"""Updates class labels in DB (connection via conn), using corresponding labels in ontology
		 (brain object ont) applied to ontology corresponding to specified using file_name."""	
		cursor1 = self.conn.cursor()
		cursor2 = self.conn.cursor()
		cursor1.execute("SELECT oc.shortFormID, oc.label FROM owl_class oc")
		dc = dict_cursor(cursor1)
		for d in dc:
			obo_id = re.sub('_', ':', d['shortFormID']) # surely there's a method that doesn't require this!
			clazo = self.ogw.getOWLClassByIdentifier(obo_id)
			new_label = self.ont.getLabel(d['shortFormID'])
			if self.ont.knowsClass(d['shortFormID']):
				if self.ogw.isObsolete(clazo):
					warnings.warn("Obsolete class: %s"  %  d['shortFormID'] )
				elif not new_label == d['label']:
					update = "UPDATE owl_class set label='%s' WHERE shortFormID = '%s'" % (new_label, d['shortFormID'])
					#print update
					cursor2.execute(update)
					#print cursor2.warnings
			else:
				warnings.warn("Unknown class: %s not in %s."  %  d['shortFormID'] )
		self.conn.commit() # without this - no updates actually get actioned!
		cursor1.close()
		cursor2.close()
		
		
	def add_owl_entity_2_db(self, shortFormId, typ):
		"""typ must be one of: owl_class; owl_objectProperty"""
		s = False
		ont_name = re.match("(\s)\_.+")  # Will fail on UUIDs!
		if typ == 'owl_objectProperty':
			if self.ont.knowsObjectProperty(shortFormId):
				s = True
		elif typ == 'owl_class':
			if self.ont.knowsClass(shortFormId):
				s = True
		else:
			warnings.warn("Unknown type, must must be one of: 'owl_class'; 'owl_objectProperty'")
			return False
		if s:	
			cursor = self.conn.cursor
			cursor.execute("INSERT IGNORE INTO %s (shortFormID, label, ontology_id) " \
                           "VALUES ('%s', '%s', %s)" % (typ, shortFormId, esc_quote(self.ont.getLabel(shortFormId)), ont_name))
			cursor.close()
			return True
		else:
			warnings.warn("Requested %s %s is not in the reference ontology!" % (typ, shortFormId))
			return False
		
					
	def _add_type(self, claz, objectProperty=False):
		"""Add to DB - a simple class expression to be used in typing.
		A simple class expression may be a single class(c), or class
		 + objectProperty (op), interpreted as op some c"""
		cursor = self.conn.cursor()
		if objectProperty:
			self.add_owl_entity_2_db(objectProperty, 'owl_objectProperty')
		self.add_owl_entity_2_db(claz, 'owl_class')
		cursor.execute("INSERT IGNORE INTO owl_type (objectProperty, class) " \
	                   "SELECT id AS objectProperty, " \
	                   "(SELECT id FROM owl_class AS class WHERE shortFormID = '%s')" \
	                    "FROM owl_objectProperty WHERE shortFormID = '%s'" % (claz, objectProperty))
		self.conn.commit()
		cursor.close()


	def add_akv_type(self, key, value, objectProperty, claz):
		if not type_exists(objectProperty, claz, self.conn):
			self._add_type(objectProperty, claz)
		typ = type_exists(objectProperty, claz)
		cursor = self.conn.cursor()
		cursor.execute("INSERT IGNORE INTO annotation_type (annotation_key_value_id, owl_type_id) " \
	                   "SELECT id AS annotation_key_value_id, '%s' AS owl_type_id " \
	                   "FROM annotation_key_value " \
	                   "WHERE annotation_class = '%s' " \
	                   "AND annotation_text = '%s'" % (typ, key, value))
		self.conn.commit()
		cursor.close()
		

		
def add_type(objectProperty, claz, conn):
	cursor = conn.cursor()
	cursor.execute("INSERT IGNORE INTO owl_type (objectProperty, class) " \
                   "SELECT id AS objectProperty, " \
                   "(SELECT id FROM owl_class AS class WHERE shortFormID = '%s')" \
                    "FROM owl_objectProperty WHERE shortFormID = '%s'" % (claz, objectProperty))
	conn.commit()
	cursor.close()
		
def add_ind_type(ind, objectProperty, claz, conn):
	"""Adds ind """
	cursor = conn.cursor()
	if not type_exists(objectProperty, claz, conn):
		add_type(objectProperty, claz, conn)
	typ = type_exists(objectProperty, claz, conn)
	cursor.execute("INSERT INTO individual_type (individual_id, type_id) SELECT oi.id AS individual_id, '%s' as type_id FROM owl_individual oi WHERE oi.shortFormID = '%s'" % (typ, ind))
	conn.commit()
	cursor.close()
	

def oe_check_db_and_add(sfid, typ, cursor, ont):
	"""Takes, sfid, owl type, cursor and ontology as Brain object as args. 
	Checks whether the sfid exists in the lmb owl_entity table, 
	finds the appropriate base URI and then adds to ont. 
	Returns true if the entity is in the table, False if not."""
	if typ not in ['owl_class', 'owl_objectProperty']:
		warnings.warn("Unknown owl type %s, please use owl_class or owl_objectProperty" % typ)
	cursor.execute("SELECT o.baseURI bu FROM ontology o JOIN %s oe ON (oe.ontology_id=o.id) WHERE shortFormID = '%s'" % (typ,sfid))
	dc = dict_cursor(cursor)
	baseURI = '' # As well as storing baseURI, serves as indicator.  Hmmm - NOT a good idea.  Refactor!  
	for d in dc:
		baseURI = d['bu'] # uniqueness constraint on table means there can be only 1  
	if baseURI:
		if typ == 'owl_class':
			ont.addClass(baseURI+sfid)
		elif typ == 'owl_objectProperty':
			ont.addObjectProperty(baseURI+sfid)
	else:
		warnings.warn("Unknown " + typ  + " " + sfid)

def BrainName_mapping(cursor, ont):
	cursor.execute("SELECT b2o.BrainName_abbv, oe.shortFormID, o.baseURI FROM BrainName_to_owl b2o JOIN owl_class oe ON (oe.id=b2o.owl_class_id) JOIN ontology o ON (o.id=oe.ontology_id)")
	BN_dict = {}
	dc = dict_cursor(cursor)
	for d in dc:
		BN = d["BrainName_abbv"]
		BN_dict[BN] = d["shortFormID"]
		if not ont.knowsClass(d["shortFormID"]):
			ont.addClass(d['baseURI'] + d["shortFormID"]) 
	return BN_dict

def gen_ind_dict(conn):
	cursor=conn.cursor()
	"""Generates a name:id dict of all individuals"""
	cursor.execute("SELECT shortFormID, label FROM owl_individual")
	dc = dict_cursor(cursor)
	id_name = {}
	for d in dc:
		id_name[d['shortFormID']] = d['label']
	return id_name
	cursor.close()


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
	conn.commit()
	cursor.close()

def add_ind_test(conn):
	cursor = conn.cursor()
	id_name = gen_ind_dict(conn)
	(vfbid, id_name, ID) = add_ind(conn, 16000, "add_ind_test", 'neuron', 'CostaJefferis', id_name)
	cursor.execute("SELECT * from owl_individual WHERE label = 'add_ind_test'")
	dc = dict_cursor(cursor)
	stat = False
	for d in dc:
		if d['label'] == "add_ind_test": 
			stat = True
	cursor.execute("DELETE from owl_individual WHERE label = 'add_ind_test'")
	conn.commit()
	cursor.close()
	return stat

def type_exists(objectProperty, claz, conn):
	cursor = conn.cursor()
	cursor.execute("SELECT ot.id FROM owl_type ot JOIN owl_objectProperty op ON (op.id=ot.objectProperty) " \
                   "JOIN owl_class oc ON (oc.id = ot.class) WHERE oc.shortFormID = '%s' AND op.shortFormID = '%s'" % (claz, objectProperty))
	dc = dict_cursor(cursor)
	typ = ''
	for d in dc:
		typ = d['id']
	cursor.close()	
	return typ



def add_ind_type_test(conn):
	cursor = conn.cursor()
	id_name = gen_ind_dict(conn)
	(vfbid, id_name, ID) = add_ind(conn, 16000, "add_ind_test", 
								'neuron', 'CostaJefferis', id_name)
	add_ind_type(vfbid, 'BFO_0000050', 'FBbt_00003624', conn)
	typ = type_exists('BFO_0000050', 'FBbt_00003624', conn)
	if not typ: 
		warnings.warn("Failed to create type statement")
	cursor.execute("SELECT type_id as tid, individual_id as iid " \
				"FROM individual_type " \
				"WHERE individual_id = '%s' " \
				"AND type_id = '%s'" % (ID, typ))
	dc = dict_cursor(cursor)
	stat = 0
	for d in dc:
		stat = d['tid'] + d['iid'] #wuh!
	if not stat:
		warnings.warn("Failed to type ind!")
	cursor.execute("DELETE FROM individual_type WHERE individual_id = '%s'" % (ID))
	conn.commit()
	cursor.execute("DELETE from owl_individual WHERE label = 'add_ind_test'")
	cursor.close()



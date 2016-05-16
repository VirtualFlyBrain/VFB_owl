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

## Notes for refactoring: 


def esc_quote(s):
	return re.sub("\'", "\\'", s)

def get_con(usr, pwd):
#	conn = zxJDBC.connect("jdbc:mysql://localhost/flycircuit",usr, pwd, "org.gjt.mm.mysql.Driver") # Use for local installation
	conn = zxJDBC.connect("jdbc:mysql://127.0.0.1:3307/flycircuit", usr, pwd, "org.gjt.mm.mysql.Driver") # To be used via ssh tunnel.
	return conn


class owlDbOnt():
	"""A class that bundles an OWL ontology with a DB handle for the VFB OWL DB.
	Methods act on the DB, rather than on the ontologies, and allow addition of 
	OWLEntities, type statements on individuals, facts etc.
	
	Individuals must be added to the DB before they are referenced.  Individuals 
	
	Classes and ObjectProperties referenced in type statements must either be:
	* present in the database
	* present in the loaded ontology
	* valid current genetic feature identifiers in FlyBase
	
	ShortForm resolution assumes the OBO short_form pattern relation to ontology name unless
	it matches pattern = 'FBtp|FBgn|FBti' - in which case FlyBase is checked.
	
	"""
	
	## Notes: The main drawback of the approach used here is speed.  
	
	
	# Aims: 
	# 1. Safely and efficiently add content to OWL DB, checking against ontology.
	#  a. Addition of simple type statements should be possible by specify shortFormID of class and (optionally) OP.
	#     Class only may be specified as class = 'pre_123456', object_Property =''  OR as just class = 'pre_123456'
	
	  
	# Should fail gracefully with an instructive error message.
	# Efficient addition means that it should be possible to add a type statement to an individual
	# even if the type statement, nor its constituent object properties or classes are currently in the DB.
	# Safety? Rather than checking, we use INSERT IGNORE + table constraints to avoid duplications in the DB.
	
	# Dealing with Null hack:
	# Background: MySQL multi-column uniqueness constraints don't work with NULL.  
	# So, to store type as named class & have uniqueness constraints, 
	# we have an OP called null_hack with shortFormID = ''.  A uniqueness constraint on shortFormID makes this safe.
	# All 
	
	# This is messy to code to, and hack to do so should be isolated.
	# TODO - come up with a clean way to hide the ugly-ness of this null hack business!
	# Make sure argument order & naming is standardised for all methods
	
	# Specs for typ
	
	
	def __init__(self, conn, ont):
		"""Conn is a zxJBDC database handle;
		ont is a Brain Object."""

		self.conn = conn  # Database connection
		self.ont = ont # Loaded ontologies (as Brain object)
		self.onto = ont.getOntology() # OWL-API ontology object
		self.ogw = OWLGraphWrapper(self.onto) #
		self.ind_IdName = {} # ID:name lookup for individuals in DB.  Updated when new individuals are generated.
		self.ind_NameId = {} # Name:ID lookup for individuals in DB.  Updated when new individuals are generated
		self._gen_ind_dicts()  # Initialise look dicts
		self.ID_range_start = 1  # ID number to start from when generating new IDs.
		self.fb_pg_conn = zxJDBC.connect("jdbc:postgresql://flybase.org/flybase" 
										,'flybase', 'flybase', "org.postgresql.Driver")  # Connection to public FlyBase.

	def __str__(self):
		return str(self.conn) + str(self.ont)

		
	def add_fb_feature(self, fbid):
		"""A FlyBase feature to DB, as specified by fbid"""
		cursor = self.fb_pg_conn.cursor()
		
		# Is this a valid, non-obsolete feature? What is its name?
		# If OK, add to DB under correct ontology.
		
		# SQL HERE NEEDS WORK!
		cursor.execute("SELECT DISTINCT f.uniquename AS fbid, synonym_sgml AS uc_name, f.is_obsolete as obstat " \
					"FROM synonym s " \
					"JOIN cvterm typ ON (typ.cvterm_id=s.type_id) " \
					"JOIN feature_synonym fs ON (fs.synonym_id=s.synonym_id) " \
					"JOIN feature f ON (f.feature_id=fs.feature_id) " \
					"WHERE f.uniquename = '%s' and fs.is_current IS TRUE and typ.name = 'symbol'" % (fbid))
		
		dc = dict_cursor(cursor)
		# Add in check for dict length?
		if dc:
			for d in dc:
				if not d['obstat']:
					self.ont.addClass(fbid) # Not worrying about baseURI here!  Adding allows lookup later.  Bit hacky.
					self.ont.label(fbid, d['uc_name'])
					self.add_owl_entity_2_db(shortFormId = fbid, typ = 'owl_class', ont_name = 'fb_feat') 
					cursor.close()
					return True
				else:
					warnings.warn("%s is an obsolete feature in FlyBase.")
					cursor.close()
					return False
		else:
			warnings.warn("%s is not in FlyBase.")
			cursor.close()
			return False
				
	def _update_akv(self):
		"""Updates the annotation_key_value table."""
		cursor = self.conn.cursor()
		cursor.execute("INSERT IGNORE INTO annotation_key_value (annotation_class, annotation_text) " \
						"SELECT DISTINCT annotation_class, text from annotation")
		self.conn.commit()
		cursor.close()

	def update_ont(self, typ): 
		"""Checks OWL classes and relations in DB for whether they Updates class or relation labels in DB using corresponding labels in ontology."""	
		cursor1 = self.conn.cursor()
		cursor2 = self.conn.cursor()
		cursor1.execute("SELECT oc.shortFormID, oc.label FROM %s oc" % typ)
		dc = dict_cursor(cursor1)
		for d in dc:
			obo_id = re.sub('_', ':', d['shortFormID']) # surely there's a method that doesn't require this!
			clazo = self.ogw.getOWLClassByIdentifier(obo_id)
			new_label = self.ont.getLabel(d['shortFormID'])
			if self.ont.knowsClass(d['shortFormID']):
				if self.ogw.isObsolete(clazo):
					warnings.warn("Obsolete class: %s"  %  d['shortFormID'] )
				elif not new_label == d['label']:
					update = "UPDATE %s set label='%s' WHERE shortFormID = '%s'" % (typ, new_label, d['shortFormID'])
					#print update
					cursor2.execute(update)
					#print cursor2.warnings
			else:
				warnings.warn("Unknown class: %s not in %s."  %  d['shortFormID'] )
		self.conn.commit() # without this - no updates actually get actioned!
		cursor1.close()
		cursor2.close()
				
	def add_owl_entity_2_db(self, shortFormId, typ, ont_name=''):
		"""Add an entity with the specified shortform ID to the database. 
		The entity is specified as typ must be one of: owl_class; owl_objectProperty.
		The entity to be added must be present in self.ontology.
		Optionally specify and ontology name, otherwise the obo standard short name 
		will be assumed - derived from the shortFormId. e.g. FBbt_00000100 => fbbt."""
		
		# Is the ontology name specified? if no, try to work out what if is by regex on ID or return a warning.
		if not ont_name:
			if re.match("(\w+)\_.+", shortFormId) :
				mung = re.match("(\w+)\_.+", shortFormId)
				ont_name = mung.group(1).lower()
			else: 
				warnings.warn("No ontology was specified for %s, and not it is not possible to derive the ontology name from the ID structure." \
						"This OWL entity must be added manually to the DB." % shortFormId)
				return False
			
		# Is the specified class/op already in the ontology.		
		s = False # in ontology ?
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
			cursor = self.conn.cursor()
			cursor.execute("INSERT IGNORE INTO %s (shortFormID, label, ontology_id) " \
	                           "VALUES (\"%s\", \"%s\", (SELECT id FROM ontology WHERE short_name = \"%s\"))" % (typ, 
								shortFormId, self.ont.getLabel(shortFormId), ont_name)) # Relies on being in ontology to get name!
			cursor.close()
			self.conn.commit()
			return True
		else:
			warnings.warn("Requested %s %s is not in the reference ontologies!" % (typ, shortFormId))
			return False
							
	def _add_type(self, OWLclass, objectProperty=''):
		"""Add to DB - a simple class expression to be used in typing.
		A simple class expression may be a single class(c), or class
		 + objectProperty (op), interpreted as op some c."""
		cursor = self.conn.cursor()

		if objectProperty:
			attempt = self.add_owl_entity_2_db(shortFormId = objectProperty, typ = 'owl_objectProperty')
			if not attempt:
				return False
		if re.match(pattern = 'FBtp|FBgn|FBti', string = OWLclass):
			self.add_fb_feature(OWLclass)
		else:
			attempt = self.add_owl_entity_2_db(OWLclass, 'owl_class')
			if not attempt:
				return False
		cursor.execute("INSERT IGNORE INTO owl_type (objectProperty, class) " \
	                   "SELECT id AS objectProperty, " \
	                   "(SELECT id FROM owl_class AS class WHERE shortFormID = '%s')" \
	                    "FROM owl_objectProperty WHERE shortFormID = '%s'" % (OWLclass, objectProperty))
		self.conn.commit()
		cursor.close()
		return True # Should be able to get status from cursor or conn -> False if INSERT fails! 

	def add_akv_type(self, key, value, OWLclass, objectProperty=''):
		self._update_akv()
		if not self.type_exists(objectProperty, OWLclass):
			self._add_type(OWLclass, objectProperty)
		typ = self.type_exists(OWLclass, objectProperty)
		cursor = self.conn.cursor()
		cursor.execute("INSERT IGNORE INTO annotation_type (annotation_key_value_id, owl_type_id) " \
	                   "SELECT id AS annotation_key_value_id, '%s' AS owl_type_id " \
	                   "FROM annotation_key_value " \
	                   "WHERE annotation_class = '%s' " \
	                   "AND annotation_text = '%s'" % (typ, key, value))
		self.conn.commit()
		cursor.close()
		
	def remove_akv_type(self, key, value, OWLclass, objectProperty=''):
		self._update_akv()
		if not self.type_exists(objectProperty, OWLclass):
			self._add_type(OWLclass, objectProperty)
		typ = self.type_exists(OWLclass, objectProperty)
		cursor = self.conn.cursor()
		cursor.execute("DELETE FROM annotation_type WHERE owl_type_id = '%s' " \
					"AND annotation_key_value_id = ( " \
					"SELECT id AS annotation_key_value_id " \
					"FROM annotation_key_value " \
	                "WHERE annotation_class = '%s' " \
	                "AND annotation_text = '%s')" % (typ, key, value))
		self.conn.commit()
		cursor.close()		
		return True
		
	def add_ind_type(self, ind, OWLclass, objectProperty=''):
		"""Adds a type statement to an individual.  
		If only class is specified, then a named class type is specified,
		otherwise the type is a class expression of the form op some c."""
		cursor = self.conn.cursor()
		typ = self.type_exists(OWLclass, objectProperty)
		if not typ:
			typ = self._add_type(OWLclass, objectProperty)
			if not typ:
				warnings.warn("Failed to type ind: %s: %s %s")
				return False
		typ = self.type_exists(OWLclass, objectProperty)
		cursor.execute("INSERT IGNORE INTO individual_type (individual_id, type_id) " \
					 "SELECT oi.id AS individual_id, '%s' AS type_id FROM owl_individual oi " \
					 " WHERE oi.shortFormID = '%s'" % (typ, ind))
		self.conn.commit()
		cursor.close()
		return typ
	
	def owl_entity_in_db(self, shortFormID, typ):
		"""Checks if owl_entity, spec as shortFormID, is in DB.
		Typ = individual, objectProperty or Class
		  Return = T/F."""
		cursor = self.conn.cursor()
		cursor.execute("SELECT * FROM owl_%s WHERE shortFormID = '%s'" % (typ, shortFormID))
		dc = dict_cursor(cursor)
		if dc:
			cursor.close()
			return True
		else:
			cursor.close()
			return False
	
	def add_fact(self, subj, rel, obj):
		"""Adds a fact statement linking two individuals.
		The relation used to link the two must be in ont.
		individuals must already be in the DB. 
		Rel must be in DB or ont.
		 Arguments specify a triple."""
		
		cursor = self.conn.cursor()
		stat = 0
		if self.owl_entity_in_db(shortFormID = subj, typ = 'individual'):
			stat = 1
		else:
			stat = 0
			warnings.warn("%s not in DB" % subj, stacklevel = 3)
		if self.owl_entity_in_db(shortFormID = obj, typ = 'individual'):
			stat = 1
		else:
			warnings.warn("%s not in DB" % obj, stacklevel = 3)
			stat = 0
		if self.owl_entity_in_db(shortFormID = rel, typ = 'objectProperty'):
			stat = 1
		elif self.ont.knowsObjectProperty(rel):
			stat = 1
		else:
			warnings.warn("%s not in DB or ontology" % rel, stacklevel = 3)
			stat = 0
		if stat:
			cursor.execute("INSERT IGNORE INTO owl_fact (subject, relation, object) VALUES (" \
							"(SELECT s.id FROM owl_individual s where s.shortFormID = '%s'), " \
							"(SELECT r.id FROM owl_objectProperty r where r.shortFormID = '%s'), " \
							"(SELECT o.id FROM owl_individual o where o.shortFormID = '%s') " \
							")" % (subj, rel, obj))
			self.conn.commit()
			cursor.close()
			return (subj, rel, obj)
		else:
			warnings.warn("Failed to add triple. Unknown components.")
			cursor.close
			return False
	
	def _gen_ind_dicts(self):
		cursor=self.conn.cursor()
		"""Generates a name:id dict of all individuals"""
		cursor.execute("SELECT shortFormID, label FROM owl_individual")
		dc = dict_cursor(cursor)
		for d in dc:
			self.ind_IdName[d['shortFormID']] = d['label']
			self.ind_NameId[d['label']] = d['shortFormID']

		cursor.close()

	def add_ind(self, name, source, ID_range_start = 0, short_name = '', idp = 'VFB', manual_spec_sfid = ''):
		"""Add an individual to the DB
		name = name of individual (string)
		source = short source name in data_source table.
		Optionally specify a start for ID range scanning 
		(otherwise defaults to self.ID_range_start).
		Using 'idp':
			Optionally specify an IDP (otherwise 'VFB' used as default)
		Using manual_spec_sfid:
			Optionally specify short form is manually (overrides ID range and idp settings)
		If individual of that name already exist, trigger warning and return False.
		Otherwise return shortFormID of newly created individual.
		"""
		cursor = self.conn.cursor()
		if manual_spec_sfid:
			vfbid = manual_spec_sfid
		else:
			if ID_range_start:
				self.ID_range_start = ID_range_start
			(vfbid, self.ID_range_start) = gen_id(idp, self.ID_range_start, 8, self.ind_IdName)			
		self.ind_IdName[vfbid] = name
		name = re.sub("'", r"\'", name) # Is this enough quotes?
		cursor.execute("SELECT oi.shortFormID from owl_individual oi WHERE oi.label = \"%s\"" % (name))
		dc = dict_cursor(cursor)
		if len(dc):
			for d in dc:
				warnings.warn("Database already has an individual called %s.  Its ID is %s." % (name, d['shortFormID']) )
			cursor.close()
			return d['shortFormID']			
		else:
			cursor.execute("INSERT IGNORE INTO owl_individual (shortFormID, uuid, label, source_id, short_name) " \
							"VALUES (\"%s\", UUID(), \"%s\", "
							"(SELECT id as source_id from data_source where name = \"%s\"), short_name)" 
							% (vfbid, name, source))
			self.conn.commit()
			cursor.close()
			return vfbid
		
	def add_linked_anatomy_image_channel(self, name, short_name, source, channel_type, background_channel, id_start_range):
		"""Adds a linked set of individuals:
		* anatomical individual
		* channel individual 
		* image individual
		
		Schema (neo4J notation)
		(anat:Individual)<-[:depicts]-(channel:Individual)
		<-[:has_signal_channel]-(image)-[:has_background_channel]-(background_channel)
		
		image-[:SUBCLASSOF]->(:Class { })
		channel-[:SUBCLASSOF]->(:Class { })
		channel-[:Type { short_form: 'OBI_', label : '' } ]->(:Class { }) % channel_type
		
		Args:
		name = name of anatomical individual
		channel_type = an fbbi term
		source = short_name of entry in data_source table
		background_channel = short_form id of background channel (e.g. registration template)
		
		returns: 
		short_form ID of anatomical individual
		
		Typing of the anatomical individual is up to implementing code."""
		
		## Generate individuals
		anat = self.add_ind(name = name, short_name = short_name, 
						source = source, ID_range_start = id_start_range)
		self.gen_image_channel_set(anat, channel_type, background_channel, id_start_range)
		return anat

	
	def gen_image_channel_set(self, anat, channel_type, background_channel, id_start_range):
		"""ARGS: 
		* anat = ID of anatomical individual
		* channel_type = { some fbbi imaging method }
		"""
		
		# Get metadata for anatomy channel - inc source and short name
		
		cur = self.conn.cursor()
		cur.execute("SELECT ds.name AS source, oi.short_name FROM owl_individual oi " \
				"JOIN data_source ds ON ds.id = oi.source_id " \
				"WHERE oi.shortFormID = '%s'" % anat)
		dc = dict_cursor(cur)
		
		for d in dc: 
			source = d['source']
			aname = d['short_name']
		# Add channel and image inds
		channel = self.add_ind(name = aname + '_c', short_name = aname + '_c', source = source, idp = 'VFBc', ID_range_start = id_start_range)
		image = self.add_ind(name = aname + '_i', short_name = aname + '_i', source = source, idp = 'VFBi', ID_range_start = id_start_range)
		
		### add facts
		self.add_fact(channel, 'depicts', anat)
		self.add_fact(image, 'VFBext_0000003', channel) # has_signal_channel
		self.add_fact(image, 'VFBext_0000002', background_channel) # has_background_channel
		
		### add types
		self.add_ind_type(ind = image, OWLclass = 'VFBext_0000006') # multi-channel image
		self.add_ind_type(ind = channel, OWLclass = 'VFBext_0000014') # channel
		self.add_ind_type(ind = channel, OWLclass = channel_type, objectProperty = 'OBI_0000312') #
		self.conn.commit()
		cur.close()

	def make_ind_obsolete(self, vfbid):
		cursor = self.conn.cursor()
		cursor.execute("UPDATE owl_individual SET is_obsolete IS TRUE WHERE shortFormID = '%s'" % vfbid)
		self.conn.commit()
		cursor.close()
				
	def type_exists(self, OWLclass, objectProperty = ''):
		"""Checks whether a type statement exist, if it does, returns the typestatement id, 
		if not, returns FLASE."""
		# Note - may not be needed if already using INSERT IGNORE.
		cursor = self.conn.cursor()
		cursor.execute("SELECT ot.id FROM owl_type ot JOIN owl_objectProperty op ON (op.id=ot.objectProperty) " \
                   "JOIN owl_class oc ON (oc.id = ot.class) WHERE oc.shortFormID = '%s' AND op.shortFormID = '%s'" %
                    (OWLclass, objectProperty))
		dc = dict_cursor(cursor)
		typ = ''
		for d in dc:
			typ = d['id']
		cursor.close()	
		return typ
	
	def ind_type_report(self, ind, ids=0):
		if ids:
			return_type = 'shortFormId'
		else:
			return_type = 'label'
			
		"""Returns an iterable of dicts with the keys
		
			d['ind'] - label/id of individual
			d['rel'] - label/id of relation in type assertion on ind
			d['claz'] - label/id of class in type assertion on ind
			
		* Default values are labels, optional ids arg switches this to shortFormIDs if true.
		* All type assertions are simple - either named class or 'R some C'
		"""
		
		cursor = self.conn.cursor()
		cursor.execute("SELECT oi.%s as ind, op.%s as rel, oc.%s as claz FROM owl_type ot " \
						"JOIN individual_type it ON (ot.id=it.type_id) " \
						"JOIN owl_individual oi ON (oi.id = it.individual_id) " \
						"JOIN owl_objectProperty op ON (op.id = ot.objectProperty) " \
						"JOIN owl_class oc ON (oc.id = ot.class) " \
						"WHERE oi.shortFormId = '%s'" % (return_type, return_type, return_type, ind))
		return dict_cursor(cursor)

	
	def gen_annotation_report(self):
		"""Returns an iterable of dicts with the keys
		
			d['annotation_class']
			d['annotation_text']
			d['op_label']
			d['op_id']
			d['class_label'] 
			d['class_id']
		
		"""
		cursor = self.conn.cursor()
		# First update AKV table
		cursor.execute("INSERT IGNORE INTO annotation_key_value (annotation_class, annotation_text) " \
		"SELECT DISTINCT annotation_class, text AS annotation_text FROM annotation")
		self.conn.commit()
		# Generate mapping doc table
		cursor.execute("SELECT akv.annotation_class, akv.annotation_text, op.label AS op_label, op.shortFormID AS op_id, " \
		"oc.label AS class_label, oc.shortFormID AS class_id " \
		"FROM annotation_key_value akv " \
		"LEFT OUTER JOIN annotation_type  at ON (akv.id = at.annotation_key_value_id) " \
		"LEFT OUTER JOIN owl_type t ON at.owl_type_id = t.id " \
		"LEFT OUTER JOIN owl_class oc ON t.class = oc.id " \
		"LEFT OUTER JOIN owl_objectProperty op ON t.objectProperty = op.id " \
		"ORDER BY annotation_class")
		return dict_cursor(cursor)
		
	

	


			
			
			
		


# def add_type(objectProperty, claz, conn):
# 	cursor = conn.cursor()
# 	cursor.execute("INSERT IGNORE INTO owl_type (objectProperty, class) " \
#                    "SELECT id AS objectProperty, " \
#                    "(SELECT id FROM owl_class AS class WHERE shortFormID = '%s')" \
#                     "FROM owl_objectProperty WHERE shortFormID = '%s'" % (claz, objectProperty))
# 	conn.commit()
# 	cursor.close()

		
# def add_ind_type(ind, objectProperty, claz, conn):
# 	"""Adds ind """
# 	cursor = conn.cursor()
# 	if not type_exists(objectProperty, claz, conn):
# 		add_type(objectProperty, claz, conn)
# 	typ = type_exists(objectProperty, claz, conn)
# 	cursor.execute("INSERT INTO individual_type (individual_id, type_id) SELECT oi.id AS individual_id, '%s' as type_id FROM owl_individual oi WHERE oi.shortFormID = '%s'" % (typ, ind))
# 	conn.commit()
# 	cursor.close()
	

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


# def gen_ind_dict(conn):
# 	cursor=conn.cursor()
# 	"""Generates a name:id dict of all individuals"""
# 	cursor.execute("SELECT shortFormID, label FROM owl_individual")
# 	dc = dict_cursor(cursor)
# 	id_name = {}
# 	for d in dc:
# 		id_name[d['shortFormID']] = d['label']
# 	return id_name
# 	cursor.close()


# def add_ind(conn, ID, name, typ, source, id_name):
# 	cursor = conn.cursor()
# 	(vfbid, ID) = gen_id('VFB', ID, 8, id_name)
# 	id_name[vfbid] = name
# 	cursor.execute("INSERT INTO owl_individual (shortFormID, uuid, label, type_for_def, source_id) VALUES ('%s', UUID(), '%s', '%s', (SELECT id as source_id from data_source where name = '%s'))" % (vfbid, name, typ, source))
# 	conn.commit()
# 	cursor.close()
# 	return (vfbid, id_name, ID)
# 	
# def make_ind_obsolete(conn, vfbid):
# 	cursor = conn.cursor()
# 	cursor.execute("UPDATE owl_individual SET is_obsolete IS TRUE WHERE shortFormID = '%s'" % vfbid)
# 	conn.commit()
# 	cursor.close()
# 
# def add_ind_test(conn):
# 	cursor = conn.cursor()
# 	id_name = gen_ind_dict(conn)
# 	(vfbid, id_name, ID) = add_ind(conn, 16000, "add_ind_test", 'neuron', 'CostaJefferis', id_name)
# 	cursor.execute("SELECT * from owl_individual WHERE label = 'add_ind_test'")
# 	dc = dict_cursor(cursor)
# 	stat = False
# 	for d in dc:
# 		if d['label'] == "add_ind_test": 
# 			stat = True
# 	cursor.execute("DELETE from owl_individual WHERE label = 'add_ind_test'")
# 	conn.commit()
# 	cursor.close()
# 	return stat
# 

# 
# 
# 
# def add_ind_type_test(conn):
# 	cursor = conn.cursor()
# 	id_name = gen_ind_dict(conn)
# 	(vfbid, id_name, ID) = add_ind(conn, 16000, "add_ind_test", 
# 								'neuron', 'CostaJefferis', id_name)
# 	add_ind_type(vfbid, 'BFO_0000050', 'FBbt_00003624', conn)
# 	typ = type_exists('BFO_0000050', 'FBbt_00003624', conn)
# 	if not typ: 
# 		warnings.warn("Failed to create type statement")
# 	cursor.execute("SELECT type_id as tid, individual_id as iid " \
# 				"FROM individual_type " \
# 				"WHERE individual_id = '%s' " \
# 				"AND type_id = '%s'" % (ID, typ))
# 	dc = dict_cursor(cursor)
# 	stat = 0
# 	for d in dc:
# 		stat = d['tid'] + d['iid'] #wuh!
# 	if not stat:
# 		warnings.warn("Failed to type ind!")
# 	cursor.execute("DELETE FROM individual_type WHERE individual_id = '%s'" % (ID))
# 	conn.commit()
# 	cursor.execute("DELETE from owl_individual WHERE label = 'add_ind_test'")
# 	cursor.close()



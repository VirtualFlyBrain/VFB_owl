#!/usr/bin/env jython
import warnings
import sys
sys.path.append('../mod') # Assuming whole repo, or at least branch under 'code', is checked out, this allows local mods to be found.
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
import obo_tools
from lmb_fc_tools import get_con

def gen_ind_by_source(cursor, vfb_ind, dataset):
	feature_ont = Brain()
	feature_ont.learn("../../owl/fb_features.owl")  # FlyBase features ontology for looking up feature names for rolling definitions.  Might be better to do this from the DB.  But that will depend on ensuring DB labels are up to date.

	class simple_classExpression:
		rel = ''
		obj = ''
	ind_id_type = {} # dict for storing lists of simple class expressions for typing individuals, indexed by sfid.
		    

    # Query for ID, name and source info for each individual
	cursor.execute("SELECT i.shortFormID AS iID, i.label AS iname, s.name as sname FROM owl_individual i JOIN data_source s ON (i.source_id=s.id) WHERE name = '%s'" % dataset)

	dc = dict_cursor(cursor)
	for d in dc:
		vfb_ind.addNamedIndividual(d['iID'])
		vfb_ind.label(d['iID'], d['iname'])
		ind_id_type[d['iID']] = []
		

	cursor.execute("SELECT i.shortFormID AS iID, oc.shortFormID AS claz, oc.label AS clazName, oeop.shortFormID AS rel, oeop.label AS relName, ontop.baseURI AS relBase, ontc.baseURI AS clazBase, s.pub_miniref, s.pub_pmid, it.for_text_def AS for_def  " \
"FROM owl_individual i  " \
"JOIN individual_type it ON (i.id=it.individual_id)  " \
"JOIN owl_type ot ON (it.type_id=ot.id)  " \
"JOIN owl_class oc ON (ot.class=oc.id)  " \
"JOIN ontology ontc ON (ontc.id=oc.ontology_id)  " \
"JOIN data_source s ON (i.source_id=s.id)  " \
"JOIN owl_objectProperty oeop ON (ot.objectProperty=oeop.id)  " \
"JOIN ontology ontop ON (ontop.id=oeop.ontology_id)  " \
"WHERE s.name = '%s' " % dataset)

	dc = dict_cursor(cursor)
	genus_class = '';
	for d in dc:
		sce = simple_classExpression() # Make object to store simple class expression
		if not vfb_ind.knowsClass(d['claz']):
			vfb_ind.addClass(d['clazBase']+d['claz'])
		if not (d['rel'] == '0'): # hack to allow mySQL combination key constraint - using OP sfid = 0 as no OP
			if not vfb_ind.knowsObjectProperty(d['rel']):
				vfb_ind.addObjectProperty(d['relBase']+d['rel'])
			vfb_ind.type(d['rel'] + ' some ' + d['claz'], d['iID'])
			sce.rel = d['rel']
			sce.obj = d['claz']
		else:
			sce.rel = ''
			sce.obj = d['claz']

			vfb_ind.type(d['claz'], d['iID'])
		ind_id_type[d['iID']].append(sce)

	for iID, types in ind_id_type.iteritems():
		definition = def_roller(types, feature_ont)
		# Now get source info.  Doing this the slow way to avoid making interim datastructure
		cursor.execute("SELECT i.shortFormID AS iID, s.name, s.pub_pmid, s.pub_miniref FROM owl_individual i JOIN data_source s ON (i.source_id=s.id) WHERE i.shortFormID = '%s'" % iID)
		source = ''
		dc = dict_cursor(cursor)
		for d in dc:
			source = d['pub_miniref'] + " (PMID:" + str(d['pub_pmid']) + ")"
		vfb_ind.annotation(iID, "IAO_0000115", definition + " " + source) # Definition
	cursor.close()

def def_roller(types, ont):
	"""Take a list of simple owl class expression objects (soce) as an arg. Each soce has 2 attributes - a relation (rel) and an object (obj).  The value of each attribute is a shortFormID"""
	genus = ''
	po = ''
	exp = ''
	defn = ''
	gender = ''
	for typ in types:
		if not typ.rel: 
			if typ.obj == 'FBbt_00005106': # neuron
				genus = 'neuron'
			elif typ.obj == 'B8C6934B-C27C-4528-BE59-E75F5B9F61B6': # expression pattern
				genus = 'expression pattern'
			elif typ.obj == 'FBbt_00007683': # neuroblast lineage clone
				genus = 'neuroblast lineage clone'
		if (typ.rel == 'BFO_0000050') & (typ.obj == 'FBbt_00003624'): # part of adult brain
			po = 'adult brain'
		if (typ.rel == 'BFO_0000050') & (typ.obj == 'FBbt_00007004'): # part male organism
				gender = 'M'
		if (typ.rel == 'BFO_0000050') & (typ.obj == 'FBbt_00007011'): # part female organism
				gender = 'F'
		if (typ.rel == 'RO_0002292'): # expresses  X
			if ont.knowsClass(typ.obj):				
				exp = ont.getLabel(typ.obj)
			else: 
				warnings.warn("%s is not a valid class in fb_features.owl. Not rolling def." % typ.obj)
			continue
	if gender == 'M':
		po = 'adult male brain'
	if gender == 'F':
		po = 'adult female brain'
	if genus == 'neuron':
		defn = "A neuron expressing %s that is part of an %s." % (exp, po)
	elif genus == 'expression pattern':
		defn = "An %s expressing %s" % (po, exp)
	elif genus == 'neuroblast lineage clone':
		defn = "An example of an %s in the %s." % (genus, po)
	return defn

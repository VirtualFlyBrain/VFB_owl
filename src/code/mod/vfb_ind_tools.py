#!/usr/bin/env jython
import warnings
import sys
sys.path.append('../mod') # Assuming whole repo, or at least branch under 'code', is checked out, this allows local mods to be found.
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
import obo_tools
from lmb_fc_tools import get_con

def load_ont(url):
	ont = Brain()
	ont.learn(url)
	return ont

def gen_ind_by_source(cursor, ont_dict, dataset):
	
	vfb_ind = ont_dict['vfb_ind']
	
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

		
	# Get source infor for this dataset
	cursor.execute("SELECT s.name, s.pub_pmid, s.pub_miniref, s.dataset_spec_text as dtext FROM data_source s WHERE s.name = '%s'" % dataset)
	dc = dict_cursor(cursor)
	for d in dc:
		 # iterate over individuals, rolling defs
		for iID, types in ind_id_type.iteritems():
			basic_def = def_roller(types, ont_dict)
			full_def = "%s from %s (PMID:%s). " % (basic_def, d['pub_miniref'], str(d['pub_pmid']))
			if d['dtext']:
				full_def += d['dtext']
			vfb_ind.annotation(iID, "IAO_0000115", full_def) # Definition
			
	# Roll image individuals.		
#	for iID in ind_id_type:
#		roll_image_ind(ont_dict['vfb_image'], dataset, vfb_ind.getLabel(iID), iID) 
	
	cursor.close()
	#

def roll_image_ind(ont, dataset, indLabel, indId):
	# stub - perhaps best called from within gen_ind_by_source?
	dataset_name_mappings = {'Jenett2012': 'Janelia2012', 'Cachero2010' : '', 'Chiang2010' : 'FlyCircuit', 'Yu2013': '', 'Ito2013' : '' }	
	dataset_name = dataset_name_mappings[dataset]
	baseURI = "http://www.virtualflybrain.org/data/thirdparty/THIRD_PARTY_INTEGRATION/%s/Thumbs/" % dataset_name
	vfbIndBase = "http://www.virtualflybrain.org/owl/" # Don't like having paths in here.  Needs to come from DB.
	image_ind =  indLabel + ".png"
	ont.addNamedIndividual(baseURI + image_ind)
	ont.type('image', image_ind)
	ont.addNamedIndividual(vfbIndBase + indId)
	ont.objectPropertyAssertion(image_ind, 'depicts',  indId)
			
def def_roller(types, ont_dict):  #
	"""Takes 2 args. ARG1: a list of simple owl class expression objects (soce) as an arg. Each source has 2 attributes - a relation (rel) and an object (obj).  The value of each attribute is a shortFormID.  ARG2: a dictionary of brain objects."""
	feat_ont = ont_dict['fb_feature']
	fbbt = ont_dict['fbbt']
	genus = '' # Generic typing
	spec_genus = '' # Specific typing for use in def.
	po = ''
	exp = ''
	defn = ''
	gender = ''
	i = 0
	for typ in types:
		if not typ.rel:
			if fbbt.isSuperClass('FBbt_00005106', typ.obj, 0):
				genus = 'neuron'
				spec_genus = fbbt.getLabel(typ.obj)
			if (typ.obj == 'FBbt_00005106'): # neuron
				genus = 'neuron'
				#			if typ.obj == 'FBbt_00003624': # adult brain - hack for EP! change back once fixed on site!!!!!!!
				if (typ.obj == 'B8C6934B-C27C-4528-BE59-E75F5B9F61B6'):
					genus = 'expression pattern' 
					# po = 'adult brain' # hack for EP! change back once fixed on site!!!!!!!
			if fbbt.isSuperClass('FBbt_00007683', typ.obj, 0) or (typ.obj == 'FBbt_00007683') : # neuroblast lineage clone
				genus = 'neuroblast lineage clone'
				spec_genus = fbbt.getLabel(typ.obj)
		if (typ.rel == 'BFO_0000050') & (typ.obj == 'FBbt_00003624'): # part of adult brain
			po = 'adult brain'
		if (typ.rel == 'BFO_0000050') & (typ.obj == 'FBbt_00007004'): # part male organism
				gender = 'M'
		if (typ.rel == 'BFO_0000050') & (typ.obj == 'FBbt_00007011'): # part female organism
				gender = 'F'
		if (typ.rel == 'RO_0002292'): # expresses  X
			if feat_ont.knowsClass(typ.obj):				
				exp = feat_ont.getLabel(typ.obj)
			else: 
				warnings.warn("%s is not a valid class in fb_features.owl. Not rolling def." % typ.obj)
			continue
	if gender == 'M':
		po = 'adult male brain'
	if gender == 'F':
		po = 'adult female brain'
	if genus == 'neuron':
		if spec_genus:
			defn = "A %s expressing %s that is part of an %s" % (spec_genus, exp, po)
		else:
			defn = "A %s expressing %s that is part of an %s" % (genus, exp, po)
	elif genus == 'expression pattern':
		defn = "An %s expressing %s" % (po, exp)
	elif genus == 'neuroblast lineage clone':
		defn = "An example of an %s in the %s" % (spec_genus, po)
	return defn


	


			
		
		
		

	

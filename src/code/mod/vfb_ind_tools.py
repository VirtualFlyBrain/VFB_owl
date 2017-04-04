#!/usr/bin/env jython
import warnings
import sys
import re
sys.path.append('../mod') # Assuming whole repo, or at least branch under 'code', is checked out, this allows local mods to be found.
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
#from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
#import obo_tools
#from lmb_fc_tools import get_con
from neo4j_tools import neo4j_connect
from owl2pdm_tools import get_types_for_ind
from owl2pdm_tools import simpleClassExpression
from java.util import TreeSet
from org.semanticweb.owlapi.model import AddAxiom



def load_ont(url):
	ont = Brain()
	ont.learn(url)
	return ont


def add_types_2_inds(ont, dc):
	"""Adds type assertions to individuals in an ontology (ont)
	as specified by a list of dicts (dc) with keys:
	iID: shortFormId of individual
	claz: shortFormId of class
	clazBase: BaseURI of claz
	rel: shortFormId of relation (set to '0' if no relation)
	relBase: BaseURI of relation"""
	for d in dc:
		if not ont.knowsClass(d['claz']):
			ont.addClass(d['clazBase']+d['claz'])
#		if not (d['rel'] == '0'): # hack to allow mySQL combination key constraint - using OP sfid = 0 as no OP
		if(d['rel']):
			if not ont.knowsObjectProperty(d['rel']):
				ont.addObjectProperty(d['relBase']+d['rel'])
			ont.type(d['rel'] + ' some ' + d['claz'], d['iID'])
		else:
			ont.type(d['claz'], d['iID'])
			
def add_facts(nc, ont, source):
	"""Adds all facts to ont for a specified source.
	"""
	r = nc.commit_list(['MATCH (s:Individual)-[r:Related]-(o:Individual) ' \
				'RETURN s.short_form AS sub, r.IRI as rel_IRI, ' \
				'r.short_form as relation, o.short_form as ob'])
	
	# transform r into dict
	
	for d in dc:
		if not ont.knowsObjectProperty(d['relation']):				
			ont.addObjectProperty(d['rel_IRI'])
		ont.objectPropertyAssertion(d['sub'], d['relation'], d['ob']) # Check Brain methods

# For now - perhaps better to hard wire with a function that generates channel/image pairs + relevant classification and facts, assuming 1:1, re-using IDs and allowing specification of a template.
# But this will almost certainly need to be 

def gen_channel_image_pair_for_ind(ont, ind, registered_to):
	"""Adds channel and image individuals to ont for ind using schema:
	image has_signal_channel channel
	image 'has_background_channel', registered_to
	channel depicts ind
	"""
	
	# Requires an existing channel for background channel.  
	acc = re.findall("VFB_(\d+)", ind)
	image_id = "VFBi_" + acc.group(2)
	channel_id = "VFBc_" + acc.group(2)
	ont.addNameIndividual(image_id)
	ont.addNameIndividual(channel_id)
	ont.addLabel(image_id, ont.getLabel(ind) + "_i")
	ont.addLabel(channel_id, ont.getLabel(ind) + "_c")
	ont.type(image_id, 'image')
	ont.type(channel_id, 'channel')	# Switch to id for rel spec
	ont.objectPropertyAssertion(image_id, 'has_signal_channel', channel_id)  # Switch to id for rel spec
	ont.objectPropertyAssertion(image_id, 'has_background_channel', registered_to) # Switch to if for rel spec
	ont.objectPropertyAssertion(channel_id, 'depicts', ind)
	

def gen_ind_by_source(nc, ont_dict, dataset):
	
	# TODO - extend to add facts
	vfb_ind = ont_dict['vfb_ind']

	# Query for ID, name and source info for each individual
	nc.execute("SELECT i.shortFormID AS iID, i.label AS iname, s.name AS sname, i.short_name," \
				"s.data_link_pre AS pre, data_link_post AS post, i.ID_in_source as extID " \
				"FROM owl_individual i JOIN data_source s ON (i.source_id=s.id) " \
				"WHERE name = '%s' AND i.shortFormID like '%s'" % (dataset, 'VFB\_%'))  # IGNORING VFBi and VFBc.

	nc.commit_list["MATCH (ds:dataset { label : '%s'} )<-[:has_data_source]-(a:Individual) " \
					"return ds, a.short_form as iID, ..."]
	dc = dict_cursor(nc)
	for d in dc:
		vfb_ind.addNamedIndividual(d['iID'])
		vfb_ind.label(d['iID'], d['iname'])
		vfb_ind.annotation(d['iID'], 'hasDbXref', 'source:' + d['sname'])
		if d['short_name']: vfb_ind.annotation(d['iID'], 'VFBext_0000004', d['short_name'])
		if d['extID']:
			if d['pre']:
				link = d['pre'] + d['extID']
			else:
				warnings.warn("%s has an external ID  (%s) but data source (%s) has no baseURI!" % 
							(d['iname'], d['extID'], d['sname']))
				continue
			if d['post']:
				link = link + d['post']
			vfb_ind.annotation(d['iID'], 'VFBext_0000005', link) #

	# Pull type statements
	nc.execute("SELECT i.shortFormID AS iID, " \
				 "oc.shortFormID AS claz, oc.label AS clazName, " \
				 "oeop.shortFormID AS rel, oeop.label AS relName, " \
				 "ontop.baseURI AS relBase, ontc.baseURI AS clazBase, " \
				 "s.pub_miniref, s.pub_pmid, it.for_text_def AS for_def  " \
				 "FROM owl_individual i  " \
				 "JOIN individual_type it ON (i.id=it.individual_id)  " \
				 "JOIN owl_type ot ON (it.type_id=ot.id)  " \
				 "JOIN owl_class oc ON (ot.class=oc.id)  " \
				 "JOIN ontology ontc ON (ontc.id=oc.ontology_id)  " \
				 "JOIN data_source s ON (i.source_id=s.id)  " \
				 "JOIN owl_objectProperty oeop ON (ot.objectProperty=oeop.id)  " \
				 "JOIN ontology ontop ON (ontop.id=oeop.ontology_id)  " \
				 "WHERE s.name = '%s' AND i.shortFormID like '%s'" % (dataset, 'VFB\_%'))

	dc = dict_cursor(nc)
	add_types_2_inds(vfb_ind, dc)
	
#	add_facts(nc, vfb_ind, dataset)

	ilist = vfb_ind.getInstances("Thing", 0)
	vfb_indo = vfb_ind.getOntology() # owl-api ontology object for typeAxioms2pdm
	
	# Get source info for this dataset
	nc.execute("SELECT s.name, s.pub_pmid, s.pub_miniref, s.dataset_spec_text as dtext " \
				"FROM data_source s WHERE s.name = '%s'" % dataset)
	
	dc = dict_cursor(nc)
	# Roll defs.
	for d in dc:
		for iID in ilist:	 
			types = get_types_for_ind("http://www.virtualflybrain.org/owl/" + iID, vfb_indo) # BaseURI should NOT be hard wired!
			defn = def_roller(types, ont_dict)
			if d['dtext']:
				defn += d['dtext']
			add_def_with_xrefs(vfb_ind, iID, defn, ["PMID:" + str(d['pub_pmid'])]) #  Ref type should not be hardwired!
						
	# Roll image individuals. Temporarily commented out.
	#	for iID in ind_id_type:
	#		roll_image_ind(ont_dict['vfb_image'], dataset, vfb_ind.getLabel(iID), iID) 
	nc.close()
	

def add_def_with_xrefs(ont, entity_sfid, def_text, xrefs):
	man = ont.manager
	dataFactory = ont.factory
	onto = ont.getOntology()
	#First build the individual axioms
	### Get APs
	defn_ap = ont.getOWLAnnotationProperty('IAO_0000115') # Definition
	xref_ap = ont.getOWLAnnotationProperty('hasDbXref') # Check that this shortform works.
	# Then roll annotations	
	# OWLAnnotation getOWLAnnotation(OWLAnnotationProperty property, OWLAnnotationValue value)
	xref_an_axioms = TreeSet()  # Is there a way to specify the type of object store from a Jython call?
	for xref in xrefs:
		val = dataFactory.getOWLLiteral(xref)
		annotation_axiom = dataFactory.getOWLAnnotation(xref_ap, val) 
		xref_an_axioms.add(annotation_axiom)		
	defn_value = dataFactory.getOWLLiteral(def_text)
	def_a = dataFactory.getOWLAnnotation(defn_ap, defn_value)
	
	# Hook def up to individual:
	#OWLAxiom axiom = this.factory.getOWLAnnotationAssertionAxiom(owlEntity.getIRI(), labelAnnotation);
	ind = ont.getOWLNamedIndividual(entity_sfid) 
	defax =  dataFactory.getOWLAnnotationAssertionAxiom(ind.getIRI(), def_a)
	# Hook def_dbxref axioms to def
	# OWLAxiom getAnnotatedAxiom(java.util.Set<OWLAnnotation> annotations)
	
	defax_an = defax.getAnnotatedAxiom(xref_an_axioms)
	#AddAxiom addAx = new AddAxiom(this.ontology, owlAxiom);
	#this.manager.applyChange(addAx);
	ax = AddAxiom(onto, defax_an)
	man.applyChange(ax)
			
def def_roller(types, ont_dict):  #
	"""Takes 2 args. ARG1: a list of simple owl class expression objects (soce) as an arg. 
	Each source has 2 attributes - a relation (rel) and an object (obj).  
	The value of each attribute is a shortFormID.  
	ARG2: a dictionary of brain objects."""
	
	# Needs to be rewritten for type pdm type objects.
	feat_ont = ont_dict['fb_feature']
	fbbt = ont_dict['fbbt']
	genus = '' # Generic typing
	spec_genus = '' # Specific typing for use in def.
	po = ''
	exp = ''
	gender = ''
	for typ in types:
		#print "Generating %s at %s" % (typ, time.gmtime())
		sce = simpleClassExpression(typ)
		if not typ.isAnonymous():
			parent_class = sce.get_class_sfid()
			if fbbt.isSuperClass('FBbt_00005106', parent_class, 0):
				genus = 'neuron'
				spec_genus = fbbt.getLabel(parent_class)
			if (parent_class == 'FBbt_00005106'): # neuron
				genus = 'neuron'
				#			if parent_class == 'FBbt_00003624': # adult brain - hack for EP! change back once fixed on site!!!!!!!
			if (parent_class == 'CARO_0030002'):
				genus = 'expression pattern' 
					# po = 'adult brain' # hack for EP! change back once fixed on site!!!!!!!
			if fbbt.isSuperClass('FBbt_00007683', parent_class, 0) or (parent_class == 'FBbt_00007683') : # neuroblast lineage clone
				genus = 'neuroblast lineage clone'
				spec_genus = fbbt.getLabel(parent_class)
		else:
			rel = sce.get_rel_sfid()
			object_class = sce.get_class_sfid()
			if (rel == 'BFO_0000050') & ( object_class== 'FBbt_00003624'): # part of adult brain
				po = 'adult brain'
				if (rel == 'BFO_0000050') & (object_class == 'FBbt_00007004'): # part male organism
					gender = 'M'
			if (rel == 'BFO_0000050') & (object_class == 'FBbt_00007011'): # part female organism
					gender = 'F'
			if (rel == 'RO_0002292'): # expresses  X
				if feat_ont.knowsClass(object_class):				
					exp = feat_ont.getLabel(object_class)
				else: 
					warnings.warn("%s is not a valid class in fb_features.owl. Not rolling def." % object_class) # Requires declaration of expression pattern class
				continue
	if gender == 'M':
		po = 'adult male brain'
	if gender == 'F':
		po = 'adult female brain'
	def_comps = ['', '', '']
	if genus == 'neuron':
		if spec_genus:
			def_comps[0] = "A %s" % spec_genus
		else:
			def_comps[0] = "A %s" % genus
		if exp:
			def_comps[1] = 'expressing %s' % exp
		if po:
			def_comps[2] = 'that is part of an %s' % po
	elif genus == 'expression pattern':
		if po and exp:
			def_comps[0] = "An %s" % po
			def_comps[1] = "expressing %s" % exp
	elif genus == 'neuroblast lineage clone':
		if spec_genus:
			def_comps[0] = "An example of a(n) %s" % spec_genus
		if po:
			def_comps[1] = "that is part of a(n) %s" % spec_genus			
	def_pre = ' '.join(def_comps)
	defn = def_pre.strip()  + '.'
	return defn

	
def roll_image_ind(ont, dataset, indLabel, indId):
	"""STUB"""
	
	# This can't work without a reliable ID scheme for individuals!
	# Ugly mapping - can ditch once this is rationalised.
	dataset_name_mappings = {'Jenett2012': 'Janelia2012', 'Cachero2010' : '', 
							'Chiang2010' : 'FlyCircuit', 'Yu2013': '', 'Ito2013' : '' }	
	dataset_name = dataset_name_mappings[dataset]
	
	baseURI = "http://www.virtualflybrain.org/data/thirdparty/THIRD_PARTY_INTEGRATION/%s/Thumbs/" % dataset_name
	vfbIndBase = "http://www.virtualflybrain.org/owl/" # Don't like having paths in here.  Needs to come from DB.
	image_ind =  indLabel + ".png"
	ont.addNamedIndividual(baseURI + image_ind)
	ont.type('image', image_ind)
	ont.addNamedIndividual(vfbIndBase + indId)
	ont.objectPropertyAssertion(image_ind, 'depicts',  indId)

			
		
		
		

	

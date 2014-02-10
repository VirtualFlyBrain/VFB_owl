#!/usr/bin/env jython

import warnings
import sys
sys.path.append('../mod') # Assuming whole repo, or at least branch under 'code', is checked out, this allows local mods to be found.
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
import obo_tools
from lmb_fc_tools import get_con
from vfb_ind_tools import def_roller


# Plan: (i) declare individuals, adding name only (Note - don't have the checking fn yet for individuals!)
#       (ii) Add typing statemnts and def (may requre rolling a datastruc for defs.


def roll_ind_by_source(cursor, vfb_ind, dataset):
	obo_tools.addOboAnnotationProperties(vfb_ind)
	feature_ont = Brain()
	feature_ont.learn("../../owl/fb_features.owl")  # FlyBase features ontology for lookging up feature names for rolling definitions.

	class simple_classExpression:
		rel = ''
		obj = ''
	ind_id_type = {} # dict for storing lists of simple class expressions for typeing individuals,, indexed by sfid.
		    

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

dataset = sys.argv[3]
vfb_ind = Brain("http://www.virtualflybrain.org/owl/", "http://www.virtualflybrain.org/owl/" + dataset + ".owl")
conn = get_con(sys.argv[1], sys.argv[2])
roll_ind_by_source(conn.cursor(), vfb_ind, dataset)
vfb_ind.save("../../owl/" + dataset + ".owl")

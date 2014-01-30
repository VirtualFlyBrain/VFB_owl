#!/usr/bin/env jython

import sys
sys.path.append('../mod') # Assuming whole repo, or at least branch under 'code', is checked out, this allows local mods to be found.
from com.ziclix.python.sql import zxJDBC # DB connection
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
import obo_tools
from lmb_fc_tools import get_con

conn = get_con(sys.argv[1], sys.argv[2])

# Plan: (i) declare individuals, adding name only (Note - don't have the checking fn yet for individuals!)
#       (ii) Add typing statemnts and def (may requre rolling a datastruc for defs.

vfb_ind = Brain("http://www.virtualflybrain.org/owl/", "http://www.virtualflybrain.org/owl/vfb_ind.owl")
obo_tools.addOboAnnotationProperties(vfb_ind)


def init_ind_by_source(cursor, vfb_ind, dataset):
	class defn: # A simple class used to create objects to store definition components
		source = '' # Source reference details
		genus = '' # Genus term for defn
		diffs = [] # list of differentia
		source_spec_text = '' # source specific text
	ind_def = {} # A dict for indexing defn objects by shortFormID

    # Query for ID, name and source info for each individual
	cursor.execute("SELECT i.shortFormID AS iID, i.label AS iname, s.name as sname, s.pub_miniref AS miniref, s.pub_pmid AS pmid, s.dataset_spec_text FROM owl_individual i JOIN data_source s ON (i.source_id=s.id) WHERE name = '%s'" % dataset)

	dc = dict_cursor(cursor)
	for d in dc:
		vfb_ind.addNamedIndividual(d['iID'])
		vfb_ind.label(d['iID'], d['iname'])
		idef = defn()
		idef.source =  d['miniref'] + " (" + str(d['pmid']) + ")"
		idef.source_spec_text = d['dataset_spec_text']
		ind_def[d['iID']] = idef
		

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
		if not vfb_ind.knowsClass(d['claz']):
			vfb_ind.addClass(d['clazBase']+d['claz'])
		if not (d['rel'] == '0'): # hack for SQL constraint- using OP sfid = 0 as no OP
			if not vfb_ind.knowsObjectProperty(d['rel']):
				vfb_ind.addObjectProperty(d['relBase']+d['rel'])
			vfb_ind.type(d['rel'] + ' some ' + d['claz'], d['iID'])
			if d['for_def']:
				ind_def[d['iID']].diffs.append(d['relName'])
		else:
			vfb_ind.type(d['claz'], d['iID'])

	for iID, idef in ind_def.iteritems():
		definition = def_roller(idef)
		vfb_ind.annotation(iID, "IAO_0000115", definition) # Definition
	cursor.close()



def def_roller(defn):
	"""Takes a defn object as an argument"""
	diff_string = ''
	while defn.diffs:
		diff_string += defn.diffs.pop()
		if len(defn.diffs) >= 1:
			diff_string += " and "		
	definition = "An example of a " + defn.genus +" " + diff_string + " from " + defn.source + ". " + defn.source_spec_text
	return definition


init_ind_by_source(conn.cursor(), vfb_ind, 'Jenett2012')

vfb_ind.save("test.owl")

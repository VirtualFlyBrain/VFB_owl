#!/usr/bin/env jython -J-Xmx4000m

import sys
sys.path.append('../mod') # Assuming whole repo, or at least branch under 'code', is checked out, this allows local mods to be found.
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
# from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
from neo4j_tools import neo4j_connect
from obo_tools import addOboAnnotationProperties, addVFBAnnotationProperties
from lmb_fc_tools import oe_check_db_and_add
from vfb_ind_tools import gen_ind_by_source
from vfb_ind_tools import load_ont
from vfb_ind_tools import add_types_2_inds

""" Use:fc_ind.py usr pwd fbbt_path
Where usr and pwd are connection credentials for LMB DB.
This script generates a file of OWL individuals representing 
FlyCircuit neurons and their clusters using the information 
in the LMB VFB mysql DB.
"""

# The rest of this code is split into functions purely for scoping, readability and documentation purposes. 
# None of the functions return, but all modify the vfb_ind brain object. 
# The init function needs to be run first as this declares 
#individuals to which Type & Fact assertions are attached by the other functions.  
#In each function, any owl entities hard coded into class expressions by the function 
#are first declared and checked against the DB.  
#A single cursor is used for each function and is used for this checking procedure, 
#so it is critical that declarations precede the main query. 
#(It is probably worth changing this to make code more robust, 
#as getting the order wrong produced incomplete output but doesn't throw an error!)


# DONE - filter out bad registrations: 
## select Name from neuron where idid NOT IN (select neuron_idid from annotation where annotation_class='process' AND text='v3bad')

def results_2_dict_list(results):
	"""Takes JSON results from a neo4J query and turns them into a list of dicts.
    """
	dc = []
	for n in results:
		# Add conditional to skip any failures
		if n:
			for d in n['data']:
				dc.append(dict(zip(n['columns'], d['row'])))
	return dc

def gen_bad_reg_list(cursor):
	"""Returns a list of idids corresponding to badly registered flycircuit"""
	cursor.execute("SELECT neuron_idid FROM annotation WHERE annotation_class='process' AND text='v3bad'")
	dc = dict_cursor(cursor)
	out = [] 
	for d in dc:
		out.append(d['neuron_idid'])
	return out


def add_manual_ann(cursor, vfb_ind):
	### NO LONGER USED ####
	"""Function to add manual typing assertions to vfb individuals."""
	
	cursor.execute("SELECT ind.shortFormID as iID, " \
				"objont.baseURI AS relBase, " \
				"rel.shortFormID as rel, " \
        		"objont.baseURI as clazBase, " \
				"oc.shortFormID as claz " \
        		"FROM owl_individual ind " \
				"JOIN neuron n ON (ind.uuid = n.uuid) " \
				"JOIN annotation a ON (n.idid=a.neuron_idid) " \
				"JOIN annotation_key_value akv ON (a.annotation_class = akv.annotation_class) " \
				"JOIN annotation_type ote ON (akv.id=ote.annotation_key_value_id) " \
				"JOIN owl_type ot on (ote.owl_type_id=ot.id) " \
				"JOIN owl_class oc ON (ot.class=oc.id) " \
				"JOIN owl_objectProperty rel ON (ot.objectProperty=rel.id) " \
				"JOIN ontology objont ON (objont.id = oc.ontology_id) " \
				"JOIN ontology relont ON (relont.id = rel.ontology_id) " \
				"WHERE a.text=akv.annotation_text " )

	dc = dict_cursor(cursor)
	add_types_2_inds(vfb_ind, dc)
	# Could add additional check against fbbt here: 
	cursor.close()
	

def add_BN_dom_overlap(nc, vfb_ind, fbbt):
	
	if not vfb_ind.knowsObjectProperty('RO_0002131'):
		vfb_ind.addObjectProperty('http://purl.obolibrary.org/obo/RO_0002131') 
	"""Function to add assertions of overlap to BrainName domains.  Currently works with a simple cutoff, but there is scope to modify this to at least specify a proportion of voxel size of domain."""
	# Note - new version is source agnostic.
	# Cypher query for overlap > 1000.
	cutoff = 1000
	s = ["MATCH (neuron:Individual)<-[:Related { short_form: 'depicts' }]-(s:Individual)" \
		"-[re:Related]->(o:Individual)-[:Related { short_form: 'depicts' }]->(x)" \
		"-[:INSTANCEOF]->(neuropil_class:Class) " \
		"WHERE re.label = 'overlaps' " \
		"AND ((re.voxel_overlap_left > %s)  " \
		"OR (re.voxel_overlap_right > %s) " \
		"OR (re.voxel_overlap_center > %s))  " \
		"RETURN properties(re) as voxel_overlap, neuron.short_form, neuron.iri, neuropil_class.short_form, neuropil_class.iri" % (cutoff, cutoff, cutoff)] # Add processing step to cypher => n
	
	# In order to support comment text generation, 
	# need to convert data structure to a dict keyed on neuron.

	r = nc.commit_list(s)
	if not r: 
		raise Exception("Neo4j query returned no results")
	overlap_results = results_2_dict_list(r)
	
	# Intermediate data-structures to add neuropils and iterate over neurons
	overlap_by_neuron = {}
	all_neuropils = set()
	for o in overlap_results:
		n = o['neuron.short_form']
		d = {'neuropil' : o['neuropil_class.short_form'],
			'voxel_overlap' : o['voxel_overlap']}
		all_neuropils.add(o['neuropil_class.iri'])
		if not (n in overlap_by_neuron.keys()):
			overlap_by_neuron[n] = []
		overlap_by_neuron[n].append(d)
	
	# Add neuropils to model				
	for n in all_neuropils: vfb_ind.addClass(n)
		
	vokeys = {'voxel_overlap_left': 'left', 
		'voxel_overlap_right' : 'right', 
		'voxel_overlap_center': ''}
			
	# Add overlaps & comments
			
	for neuron, overlaps in overlap_by_neuron.items():
		neuron_overlap_txt  = []
		# Iterate over neuropils.
		for o in overlaps:
			voxel_overlap = o['voxel_overlap'] 
			typ = "RO_0002131 some %s" % o['neuropil']
			vfb_ind.type(typ,neuron)
			txt = "Overlap of %s inferred from " % fbbt.getLabel(o['neuropil'])
			vo_data = []
			for k,v in vokeys.items():
				if k in voxel_overlap.keys() and voxel_overlap[k] > cutoff:
					vo_data.append("%d voxel overlap of the %s %s"  % (voxel_overlap[k], v, fbbt.getLabel(o['neuropil']))) # Better to ref painted domain?
			neuron_overlap_txt.append(txt + ', '.join(vo_data))
		vfb_ind.comment(neuron, '. '.join(neuron_overlap_txt) + '.')

def add_clusters(nc, vfb_ind):
	

	""" Declare cluster individuals """

	# TODO: Add typing to clusters.
	# Temp ID as UUID.  This one can be safely switched to an RO ID as individual queries on the site currently work on labels (!)
	# Should just be able to add as part of loop without any extra check.
#	oe_check_db_and_add('c099d9d6-4ef3-11e3-9da7-b1ad5291e0b0', 'owl_objectProperty', cursor, vfb_ind)
#	oe_check_db_and_add('C888C3DB-AEFA-447F-BD4C-858DFE33DBE7', 'owl_objectProperty', cursor, vfb_ind)
#	oe_check_db_and_add('VFB_10000005', 'owl_class', cursor, vfb_ind)
#   Loop used in vfb_ind_tools:
# 		if not vfb_ind.knowsClass(d['claz']):
# 			vfb_ind.addClass(d['cIRI'])
# 		if(d['edge_type'] == 'Related'):
# 			if not vfb_ind.knowsObjectProperty(d['rel']):
# 				vfb_ind.addObjectProperty(d['rel_IRI'])
# 			vfb_ind.type(d['rel'] + ' some ' + d['claz'], d['iID'])
# 		elif (d['edge_type'] == 'INSTANCEOF'):
# 			vfb_ind.type(d['claz'], d['iID'])
# 		else:
# 			warnings.warn("Unknown edge type: %s in triple %s, %s, %s"  % (d['edge_type'], d['iID'], d['rel'], d['claz']) )

	r = nc.commit_list(["MATCH (ds:DataSet) WHERE ds.label = '' " \
					"with ci (cc:Class)<-[:INSTANCEOF]-(ci)<-[r:Related]-(n:Individual) " \
					"WHERE cc.label = 'cluster' AND r.label = 'member_of' " \
					"RETURN cc.iri as cluster_class, ci.iri as cluster_ind, ci.label as cluster_ind_label " \
					"ci.label"]) # How to restrict to V3.  
	# I think this can be done on dataSet. CHECK
	dc = results_2_dict_list(r)
	# Now iterate over adding member_of / has_member reciprocals.  Would be good to add some standard text too.  
	
#	cursor.execute("SELECT DISTINCT ind.shortFormID as cvid, c.cluster as cnum, eind.shortFormID as evid, c.clusterv as cversion " \
# 				   "FROM owl_individual ind " \
# 				   "JOIN cluster c ON (ind.uuid=c.uuid) " \
# 				   "JOIN clustering cg ON (cg.cluster=c.cluster) " \
# 				   "JOIN neuron n ON (cg.exemplar_idid=n.idid) " \
# 				   "JOIN owl_individual eind ON (n.uuid=eind.uuid) " \
# 				   "WHERE cg.clusterv_id = c.clusterv " \
# 				   "AND ind.type_for_def  = 'cluster' " \
# 				   "AND c.clusterv = '3'")

	for d in dc:
		if not vfb_ind.knowsClass(d["cvid"]):
			vfb_ind.addNamedIndividual(d["cvid"])
			vfb_ind.type('VFB_10000005', d["cvid"])
			vfb_ind.label(d["cvid"], "cluster " + str(d["cversion"]) + "." + str(d["cnum"])) # Note ints returned by query need to be coerced into strings.
			vfb_ind.objectPropertyAssertion(d["evid"], "c099d9d6-4ef3-11e3-9da7-b1ad5291e0b0", d["cvid"]) # UUID for exemplar as a placeholder - awaiting addition to RO
			vfb_ind.objectPropertyAssertion(d["cvid"], "C888C3DB-AEFA-447F-BD4C-858DFE33DBE7", d["evid"]) # UUID for exemplar as a placeholder - awaiting addition to RO

#	cursor.close()

def map_to_clusters(cursor, vfb_ind):
	"""Maps fc individuals to clusters"""

	oe_check_db_and_add("RO_0002351", 'owl_objectProperty', cursor, vfb_ind) #  has_member
	oe_check_db_and_add("RO_0002350", 'owl_objectProperty', cursor, vfb_ind)  #  member_of

	cursor.execute("SELECT DISTINCT cind.shortFormID AS cvid, nind.shortFormID AS mvid " \
				   "FROM clustering cg " \
				   "JOIN neuron n ON (cg.idid=n.idid) " \
				   "JOIN owl_individual nind ON (n.uuid=nind.uuid) " \
				   "JOIN cluster c ON (cg.cluster=c.cluster) " \
				   "JOIN owl_individual cind ON (c.uuid=cind.uuid) " \
				   "WHERE c.clusterv = cg.clusterv_id " \
				   "AND cg.clusterv_id = '3'") # It is essential to set clustering version twice ! (crappy schema...)

	# Now add cluster assertions.  Note - these are declared in both directions as elk cannot cope with inverses.

	dc = dict_cursor(cursor)
	for d in dc:
		vfb_ind.objectPropertyAssertion(d['cvid'], "RO_0002351" ,d['mvid']) 
		vfb_ind.objectPropertyAssertion(d['mvid'], "RO_0002350", d['cvid'])

	cursor.close()

# Initialise brain object for vfb individuals, and add declarations of OBO-style object property 

#conn = get_con(sys.argv[1], sys.argv[2])
nc = neo4j_connect(sys.argv[1], sys.argv[2], sys.argv[3])
FBBT = sys.argv[4]
dataset = 'Chiang2010'
# cursor = conn.cursor()
# cursor.execute("SELECT baseURI FROM ontology where short_name = 'vfb_ind'")
# dc = dict_cursor(cursor)
# baseURI = ''
# for d in dc:
# 	baseURI = d['baseURI']
# cursor.close()
vfb_ind = Brain('http://www.virtualflybrain.org/owl/', 'http://www.virtualflybrain.org/owl/' + 'flycircuit_plus.owl') # Adding IRI manually for now.
# Setup ontologies
addOboAnnotationProperties(vfb_ind)
addVFBAnnotationProperties(vfb_ind)
ont_dict = {}
ont_dict['vfb_ind']=vfb_ind
ont_dict['fbbt'] = load_ont(FBBT)
#ont_dict['fbbt'] = load_ont("http://purl.obolibrary.org/obo/fbbt/%s/fbbt-simple.owl" % fbbt_release_version)
ont_dict['fb_feature'] = load_ont("../../owl/fb_features.owl")
#ont_dict['fb_feature'] = load_ont("http://purl.obolibrary.org/obo/fbbt/vfb/fb_features.owl")
# Now run all the functions

gen_ind_by_source(nc, ont_dict, dataset)
#add_manual_ann(conn.cursor(), vfb_ind)
add_BN_dom_overlap(nc, vfb_ind, ont_dict['fbbt'])
#add_clusters(nc, vfb_ind) Temporarily commenting to test voxel overlp function.
#map_to_clusters(nc, vfb_ind)


# Save output file and clean up

vfb_ind.save("../../owl/flycircuit_plus.owl")
#conn.close()
vfb_ind.sleep()
ont_dict['fbbt'].sleep()
ont_dict['fb_feature'].sleep()

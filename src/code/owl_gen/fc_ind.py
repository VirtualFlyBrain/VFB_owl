#!/usr/bin/env jython -J-Xmx4000m

import sys
sys.path.append('../mod') # Assuming whole repo, or at least branch under 'code', is checked out, this allows local mods to be found.
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
# from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
from obo_tools import addOboAnnotationProperties, addVFBAnnotationProperties
from lmb_fc_tools import oe_check_db_and_add
from lmb_fc_tools import BrainName_mapping
from lmb_fc_tools import get_con
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
	"""Function to add assertions of overlap to BrainName domains.  Currently works with a simple cutoff, but there is scope to modify this to at least specify a proportion of voxel size of domain."""
	# Note - new version is source agnostic.
	# Cypher query for overlap > 1000.
	cutoff = 1000
	s = ["MATCH (neuron:Individual)<-[d1:Related]- " \
			"(s:Individual)-[re:Related]->(o:Individual)" \
			"->[d2:Related]-(Individual:neuropil)-[:INSTANCEOF]->(neuropil_class:Class) " \
			"WHERE d1.short_form = 'depicts" \
			"AND d2.short_form = 'depicts" \
			"((re.voxel_overlap_left > %d)  " \
			"OR (re.voxel_overlap_right > %d) " \
			"OR (re.voxel_overlap_center > %d))  " \
			"RETURN DISTINCT neuron.short_form , neuropil_class.short_form, properties(re) as voxel_overlap" 
			% (cutoff, cutoff, cutoff)]  # Add processing step to cypher => n
	
	# In order to support comment text generation, 
	# need to convert data structure to a dict keyed on neuron.

	r = nc.commit_list(s)
	overlap_results = results_2_dict_list(r)
	oe_check_db_and_add("RO_0002131", 'owl_objectProperty', cursor, vfb_ind)
	voxel_overlap = overlap_results['voxel_overlap']
	voxel_overlap_txt = ''
	overlap_by_neuron = {}
	for o in overlap_results:
		n = o['neuron.short_form']
		d = {'neuropil' : o['neuropil_class.short_form'],
			'voxel_overlap' : o['voxel_overlap']}
		if not (n in overlap_by_neuron.keys()):
			overlap_by_neuron[n] = []
		overlap_by_neuron[n].append(d)
					
	
	vokeys = {'voxel_overlap_left': 'left', 
		'voxel_overlap_right' : 'right', 
		'voxel_overlap_center': ''}
			
			
	for neuron, overlaps in overlap_by_neuron.items():
		voxel_overlap_txt = ''
		for o in overlaps: 
			typ = "RO_0002131 some <%s>" % o['neuropil']
			vfb_ind.type(typ,neuron)
			voxel_overlap_txt += "Overlap of %s inferred from: " % fbbt.getLabel(o['neuropil'])
			vo_data = []
		for k,v in vokeys.items():
			if k in voxel_overlap.keys() and voxel_overlap[k] > cutoff:
				vo_data.append()
				voxel_overlap_txt += "%s voxel overlap of %d"  % (v, k) # Txt may need work.
		voxel_overlap_txt += '; '.join(vo_data) + '.'
		vfb_ind.comment(neuron, voxel_overlap_txt)


def add_clusters(cursor, vfb_ind):

	""" Declare cluster individuals """

	# TODO: Add typing to clusters.

	# Temp ID as UUID.  This one can be safely switched to an RO ID as individual queries on the site currently work on labels (!)
	oe_check_db_and_add('c099d9d6-4ef3-11e3-9da7-b1ad5291e0b0', 'owl_objectProperty', cursor, vfb_ind)
	oe_check_db_and_add('C888C3DB-AEFA-447F-BD4C-858DFE33DBE7', 'owl_objectProperty', cursor, vfb_ind)
	oe_check_db_and_add('VFB_10000005', 'owl_class', cursor, vfb_ind)

	cursor.execute("SELECT DISTINCT ind.shortFormID as cvid, c.cluster as cnum, eind.shortFormID as evid, c.clusterv as cversion " \
				   "FROM owl_individual ind " \
				   "JOIN cluster c ON (ind.uuid=c.uuid) " \
				   "JOIN clustering cg ON (cg.cluster=c.cluster) " \
				   "JOIN neuron n ON (cg.exemplar_idid=n.idid) " \
				   "JOIN owl_individual eind ON (n.uuid=eind.uuid) " \
				   "WHERE cg.clusterv_id = c.clusterv " \
				   "AND ind.type_for_def  = 'cluster' " \
				   "AND c.clusterv = '3'")

	dc = dict_cursor(cursor)
	for d in dc:
		if not vfb_ind.knowsClass(d["cvid"]):
			vfb_ind.addNamedIndividual(d["cvid"])
			vfb_ind.type('VFB_10000005', d["cvid"])
			vfb_ind.label(d["cvid"], "cluster " + str(d["cversion"]) + "." + str(d["cnum"])) # Note ints returned by query need to be coerced into strings.
			vfb_ind.objectPropertyAssertion(d["evid"], "c099d9d6-4ef3-11e3-9da7-b1ad5291e0b0", d["cvid"]) # UUID for exemplar as a placeholder - awaiting addition to RO
			vfb_ind.objectPropertyAssertion(d["cvid"], "C888C3DB-AEFA-447F-BD4C-858DFE33DBE7", d["evid"]) # UUID for exemplar as a placeholder - awaiting addition to RO

	cursor.close()

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

conn = get_con(sys.argv[1], sys.argv[2])
FBBT = sys.argv[3]
dataset = 'Chiang2010'
cursor = conn.cursor()
cursor.execute("SELECT baseURI FROM ontology where short_name = 'vfb_ind'")
dc = dict_cursor(cursor)
baseURI = ''
for d in dc:
	baseURI = d['baseURI']
cursor.close()
vfb_ind = Brain(baseURI, baseURI + 'flycircuit_plus.owl')
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

gen_ind_by_source(conn.cursor(), ont_dict, dataset)
add_manual_ann(conn.cursor(), vfb_ind)
add_BN_dom_overlap(conn.cursor(), vfb_ind, ont_dict['fbbt'])
add_clusters(conn.cursor(), vfb_ind)
map_to_clusters(conn.cursor(), vfb_ind)


# Save output file and clean up

vfb_ind.save("../../owl/flycircuit_plus.owl")
conn.close()
vfb_ind.sleep()
ont_dict['fbbt'].sleep()
ont_dict['fb_feature'].sleep()

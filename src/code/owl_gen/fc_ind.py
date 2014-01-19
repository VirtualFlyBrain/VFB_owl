#!/usr/bin/env jython

import sys
from com.ziclix.python.sql import zxJDBC # DB connection
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
import obo_tools
from lmb_fc_tools import oe_check_db_and_add
from lmb_fc_tools import BrainName_mapping

# TODO - Add warnings if entity checks against DB fail
# TODO - Split into modules with textual descriptions for each bit

conn = zxJDBC.connect("jdbc:mysql://localhost/flycircuit", sys.argv[1], sys.argv[2], "org.gjt.mm.mysql.Driver") # For local testing
#conn = zxJDBC.connect("jdbc:mysql://127.0.0.1:3307/flycircuit", sys.argv[1], sys.argv[2], "org.gjt.mm.mysql.Driver") # To be used via ssh tunnel.

cursor = conn.cursor()

# Brain objects - global
fbbt = Brain()
#fbbt.learn("http://purl.obolibrary.org/fbbt/fbbt-simple.owl")
#fbbt.learn("file:///repos/fbbtdv/fbbt/releases/fbbt-simple.owl") # local path for debugging.  Replace by URL above to make generic
vfb_ind = Brain("http://www.virtualflybrain.org/owl/", "http://www.virtualflybrain.org/owl/vfb_ind.owl")

obo_tools.addOboAnnotationProperties(vfb_ind)

# Temporary hard coding. Should probably add something to DB to encode these patterns!

oe_check_db_and_add('BFO_0000050', 'objectProperty', cursor, vfb_ind)
oe_check_db_and_add('FBbt_00005106', 'class', cursor, vfb_ind)
oe_check_db_and_add('FBbt_00003624', 'class', cursor, vfb_ind)
oe_check_db_and_add('FBbt_00007004', 'class', cursor, vfb_ind)
oe_check_db_and_add('FBbt_00007011', 'class', cursor, vfb_ind)
oe_check_db_and_add('RO_0002292', 'objectProperty', cursor, vfb_ind) # expresses


cursor.execute("SELECT vut.vfbid as vid, n.name, n.Gender, n.gene_name, oe.shortFormID as DriverSFID, oe.label as Driver " \
"FROM neuron n " \
"JOIN vfbid_uuid_type vut ON (n.uuid=vut.uuid) " \
"JOIN flycircuit_driver_map fdm ON (n.Driver = fdm.fc_name) " \
"JOIN owl_entity oe ON (fdm.owl_entity_id=oe.id)")
dc = dict_cursor(cursor)
cursor2 = conn.cursor() # temporary fix for passing cursor  Seem to have a problem with nesting of cursors due to the way dict_cursor works.
for d in dc:
	vfb_ind.addNamedIndividual(d['vid'])
	vfb_ind.label(d['vid'], d['name'])
	vfb_ind.type('FBbt_00005106', d['vid'])  #  default typing as neuron
	vfb_ind.type("BFO_0000050 some FBbt_00003624", d['vid'])  # default typing as part of some 'adult brain'
	defn = "A neuron of an " # Begin rolling def.
	if d['Gender'] == 'M':
		vfb_ind.type("BFO_0000050 some FBbt_00007004", d['vid'])  # Part of some male organism
		defn += "adult male brain "
	if d['Gender'] == 'F':
		vfb_ind.type("BFO_0000050 some FBbt_00007011", d['vid'])  # Part of some female organism
		defn += "adult female brain "
	vfb_ind.annotation(d['vid'], "hasExactSynonym", d['gene_name']) 	#  Add gene_name as exact synonym.  Note, shortFormID on splits on '#'
	defn += " expressing " + d['Driver'] + "."
	if not vfb_ind.knowsClass(d['DriverSFID']):
		oe_check_db_and_add(d['DriverSFID'], 'class', cursor2, vfb_ind)
	vfb_ind.type("RO_0002292 some " + d['DriverSFID'], d['vid'])
	vfb_ind.annotation(d['vid'], "IAO_0000115", defn) # Definition


# Add manual annotation assertions:

cursor.execute("SELECT vut.vfbid as vid, relont.baseURI AS relBase, rel.ShortFormID as rel, objont.baseURI as clazBase, obj.shortFormID as claz " \
"FROM vfbid_uuid_type vut " \
"JOIN neuron n ON (vut.uuid = n.uuid) " \
"JOIN annotation a ON (n.idid=a.neuron_idid) " \
"JOIN annotation_key_value akv ON (a.annotation_class = akv.annotation_class) " \
"JOIN annotation_to_owl ote ON (akv.id=ote.annotation_key_value_id) " \
"JOIN owl_entity obj ON (ote.class=obj.id) " \
"JOIN ontology objont ON (objont.ontology_id = obj.ontology) " \
"LEFT OUTER JOIN owl_entity rel ON (ote.objectProperty=rel.id) " \
"LEFT OUTER JOIN ontology relont ON (relont.ontology_id=rel.ontology) " \
"WHERE a.text=akv.annotation_text")

dc = dict_cursor(cursor)

for d in dc:
	if not vfb_ind.knowsClass(d['claz']):
		vfb_ind.addClass(d['clazBase']+d['claz'])
	if d['rel']:
		if not vfb_ind.knowsObjectProperty(d['rel']):
			vfb_ind.addObjectProperty(d['relBase']+d['rel'])
		vfb_ind.type(d['rel'] + ' some ' + d['claz'], d['vid'])
	else:
	   vfb_ind.type(d['claz'], d['vid'])

# Roll lookup for BrainName shorthand:

BN_dict = BrainName_mapping(cursor, vfb_ind)  # Guess there's no harm in this being global, but could limit scope...
#print BN_dict
BN_abbv_list = BN_dict.keys()


# Adding typing based on domain overlap

cursor.execute("SELECT vut.vfbid as vid, sj.* " \
			   "FROM spatdist_jfrc sj " \
			   "JOIN neuron n ON (sj.idid=n.idid) " \
			   "JOIN vfbid_uuid_type vut ON (n.uuid=vut.uuid)")

oe_check_db_and_add("RO_0002131", 'objectProperty', cursor, vfb_ind)

dc = dict_cursor(cursor)
for d in dc:
	above_cutoff = {} # Dict containing all domains above cutoff as keys and the voxel overlap as value
	voxel_overlap_txt = "From analysis of a registered 3D image, this neuron is predicted to overlap the following neuropils: "
	for abbv in BN_abbv_list:
		if d[abbv] > 1000:  # Using crude cutoff for now - but could make this ratio based instead, given data from Marta.
			above_cutoff[BN_dict[abbv]] = (d[abbv])
	while above_cutoff:
		dom = above_cutoff.popitem()  # pop item from dict (dom now has a list of key, value)
		typ = "RO_0002131 some " + dom[0]
		vfb_ind.type(typ,d["vid"])
		voxel_overlap_txt += str(dom[1]) + " voxels overlap the " + fbbt.getLabel(dom[0])   
		if len(above_cutoff) >= 1:  # Equivalent for keys with iterable?
			voxel_overlap_txt +=  "; "
		else:
			 voxel_overlap_txt += "."
	vfb_ind.comment(d['vid'], voxel_overlap_txt)

# Adding clusters               

cursor.execute("SELECT DISTINCT vut.vfbid as cvid, c.cluster as cnum, evut.vfbid as evid, c.clusterv as cversion " \
			   "FROM vfbid_uuid_type vut " \
			   "JOIN cluster c ON (vut.uuid=c.uuid) " \
			   "JOIN clustering cg ON (cg.cluster=c.cluster) " \
			   "JOIN neuron n ON (cg.exemplar_idid=n.idid) " \
			   "JOIN vfbid_uuid_type evut ON (n.uuid=evut.uuid) " \
			   "WHERE cg.clusterv_id = c.clusterv " \
			   "AND vut.type = 'cluster' " \
			   "AND c.clusterv = '3'")

# Note on IDs: At the time of writing this script, queries on individuals all work via OWLtools MS queries with labels. So, labels need to be stable for everything to keep working, but IDs do not.

oe_check_db_and_add("c099d9d6-4ef3-11e3-9da7-b1ad5291e0b0", 'objectProperty', cursor, vfb_ind)


dc = dict_cursor(cursor)
for d in dc:
	if not vfb_ind.knowsClass(d["cvid"]):
		vfb_ind.addNamedIndividual(d["cvid"])
		vfb_ind.label(d["cvid"], "cluster " + str(d["cversion"]) + "." + str(d["cnum"])) # Note ints returned by query need to be coerced into strings.
		vfb_ind.objectPropertyAssertion(d["evid"], "c099d9d6-4ef3-11e3-9da7-b1ad5291e0b0", d["cvid"]) # UUID for exemplar as a placeholder - awaiting addition to RO

# Add cluster membership

cursor.execute("SELECT DISTINCT cvut.vfbid AS cvid, nvut.vfbid AS mvid " \
			   "FROM clustering cg " \
			   "JOIN neuron n ON (cg.idid=n.idid) " \
			   "JOIN vfbid_uuid_type nvut ON (n.uuid=nvut.uuid) " \
			   "JOIN cluster c ON (cg.cluster=c.cluster)" \
			   "JOIN vfbid_uuid_type cvut ON (c.uuid=cvut.uuid)" \
			   "WHERE c.clusterv = '3'")

oe_check_db_and_add("RO_0002351", 'objectProperty', cursor, vfb_ind)
oe_check_db_and_add("RO_0002350", 'objectProperty', cursor, vfb_ind)

# Now add cluster assertions...


      
cursor.close()
conn.close()

vfb_ind.save("vfb_ind.owl") 

#!/usr/bin/env jython

import sys
from com.ziclix.python.sql import zxJDBC # DB connection
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
import obo_tools

conn = zxJDBC.connect("jdbc:mysql://localhost/flycircuit", sys.argv[1], sys.argv[2], "org.gjt.mm.mysql.Driver")
cursor = conn.cursor()

# Brain objects - global
fbbt = Brain()
#fbbt.learn("http://purl.obolibrary.org/fbbt/fbbt-simple.owl")
fbbt.learn("file:///repos/fbbtdv/fbbt/releases/fbbt-simple.owl") # local path for debugging.  Replace by URL above to make generic
vfb_ind = Brain("http://www.virtualflybrain.org/owl/", "http://www.virtualflybrain.org/owl/vfb_ind.owl")

obo_tools.addOboAnnotationProperties(vfb_ind)

# Temporary hard coding. Should really add something to DB to encode these patterns!


cursor.execute("SELECT vut.vfbid as vid, n.name, n.Gender, n.gene_name, Driver FROM neuron n JOIN vfbid_uuid_type vut ON (n.uuid=vut.uuid)")
dc = dict_cursor(cursor)
for d in dc:
	vfb_ind.addNamedIndividual(d['vid'])
	vfb_ind.label(d['vid'], d['name'])
	vfb_ind.addClass('http://purl.obolibrary.org/obo/FBbt_00005106')
	vfb_ind.addObjectProperty('http://purl.obolibrary.org/obo/BFO_0000050')
	vfb_ind.type('FBbt_00005106', d['vid'])  #  default typing as neuron
	vfb_ind.type("BFO_0000050 some FBbt_00003624", d['vid'])  # default typing as part of some 'adult brain'
	vfb_ind.addClass('http://purl.obolibrary.org/obo/FBbt_00003624')
	defn = "A neuron of an " # Begin rolling def.
	if d['Gender'] == 'M':
		vfb_ind.addClass('http://purl.obolibrary.org/obo/FBbt_00007004')
		vfb_ind.type("BFO_0000050 some FBbt_00007004", d['vid'])  # Part of some male organism
		defn += "adult male brain "
	if d['Gender'] == 'F':
		vfb_ind.addClass('http://purl.obolibrary.org/obo/FBbt_00007011')
		vfb_ind.type("BFO_0000050 some FBbt_00007011", d['vid'])  # Part of some female organism
		defn += "adult female brain "
	vfb_ind.annotation(d['vid'], "hasExactSynonym", d['gene_name']) 	#  Add gene_name as exact synonym.  Note shortFormID on splits on '#'
	defn += " expressing " + d['Driver'] + "." # Need a lookup for Driver name to FB.
	vfb_ind.annotation(d['vid'], "IAO_0000115", defn) # Start rolling def 	
	# Add expresssion assertion

cursor.execute("SELECT vut.vfbid as vid, rel.baseURI AS relBase, rel.ShortFormID as rel, obj.baseURI as clazBase, obj.shortFormID as claz " \
"FROM vfbid_uuid_type vut " \
"JOIN neuron n ON (vut.uuid = n.uuid) " \
"JOIN annotation a ON (n.idid=a.neuron_idid) " \
"JOIN annotation_key_value akv ON (a.annotation_class = akv.annotation_class) " \
"JOIN annotation_to_owl ote ON (akv.id=ote.annotation_key_value_id) " \
"JOIN owl_entity obj ON (ote.class=obj.id) " \
"LEFT OUTER JOIN owl_entity rel ON (ote.objectProperty=rel.id) " \
"WHERE a.text=akv.annotation_text")

# Should make this into a function.

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
      
cursor.close()
conn.close()

vfb_ind.save("vfb_ind.owl") 

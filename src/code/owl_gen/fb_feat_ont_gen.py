#!/usr/bin/env jython

import sys
sys.path.append('../mod') # Assuming whole repo, or at least branch under 'code', is checked out, this allows local mods to be found.
from com.ziclix.python.sql import zxJDBC # DB connection
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
from uk.ac.ebi.brain.core import Brain
from neo4j_tools import neo4j_connect
# import lmb_fc_tools
import re
import warnings
import time


def neo_json_2_dict(r):
	"""
	Takes JSON results from a neo4J query and turns them into a table.
	Only works for queries returning keyed attributes"""
	### Only works for queries returning keyed attributes!
	dc = []
	for n in r[0]['data']:
		dc.append(dict(zip(r[0]['columns'], n['row'])))
	return dc


fbf = "http://purl.obolibrary.org/fbbt/fbfeat/fb_features.owl"
fbf_base = "http://flybase.org/reports/"
obo_base = "http://purl.obolibrary.org/obo/"

fb_feature = Brain(fbf_base, fbf)  # Should really be pulling full URIs here!

# declaration of parent classes for FB features and expression patterns
# Shouldn't really be adding labels here...

fb_feature.addClass(obo_base + "SO_0000704")
fb_feature.label("SO_0000704", "gene")
fb_feature.addClass(obo_base + 'SO_0000796')
fb_feature.label('SO_0000796', "transgenic_transposable_element")
fb_feature.addClass(obo_base + "SO_0001218")
fb_feature.label("SO_0001218", "transgenic_insertion")
fb_feature.addClass(obo_base + "SO_0001023")
fb_feature.label("SO_0001023", "allele")

fb_feature.addClass(obo_base + "CARO_0030002")
fb_feature.label("CARO_0030002", "expression pattern")

nc = neo4j_connect(sys.argv[1], sys.argv[2], sys.argv[3])
#fb_pg_conn = zxJDBC.connect("jdbc:postgresql://bocian.inf.ed.ac.uk/flybase" + "?ssl=true" + "&sslfactory=org.postgresql.ssl.NonValidatingFactory" 
#					, sys.argv[3], sys.argv[4], "org.postgresql.Driver") 

fb_pg_conn = zxJDBC.connect("jdbc:postgresql://chado.flybase.org/flybase", 
					'flybase', '', "org.postgresql.Driver") # public DB

#vfb_cursor = vfb_ms_conn.cursor()
fb_cursor = fb_pg_conn.cursor()

#vfb_cursor.execute("SELECT oc.shortFormID FROM owl_class oc " \
#				"JOIN ontology o ON (oc.ontology_id=o.id)" \
#				" WHERE o.URI = '%s'" % (fbf))

feature_result = nc.commit_list(["MATCH (f:Feature)-[r]-(i:Individual) RETURN f.IRI, f.short_form"])

flist = []
dc = neo_json_2_dict(feature_result)
for d in dc:
	flist.append(d['f.short_form'])
# Need to chunk list up - try chunks of 100 + short pause between.

def chunks(l, n):
	"""Yield successive n-sized chunks from l."""
	for i in xrange(0, len(l), n):
		yield l[i:i+n]

class_lists = chunks(l = flist, n = 100)

# Need to be careful to preserve UTF-8 content here!
for cl in class_lists:
	class_list_string = "'" + "', '".join(cl) + "'"	
	query = "SELECT DISTINCT f.uniquename AS fbid, synonym_sgml AS uc_name, f.is_obsolete as obstat " \
	"FROM synonym s " \
	"JOIN cvterm typ ON (typ.cvterm_id=s.type_id) " \
	"JOIN feature_synonym fs ON (fs.synonym_id=s.synonym_id) " \
	"JOIN feature f ON (f.feature_id=fs.feature_id) " \
	"WHERE f.uniquename in (%s) and fs.is_current IS TRUE and typ.name = 'symbol'" % (class_list_string)
	
	fb_cursor.execute(query)  # 
	
	fb_dc = dict_cursor(fb_cursor)
	for fb in fb_dc:
#		print "\nProcessing:" + fb['uc_name']
		if fb['obstat']:
			warnings.warn(fb['fbid'] +" " + fb['uc_name'] + " is obsolete !  Not adding to fb_feature.owl.") 
		else:
			if not fb_feature.knowsClass(fb['fbid']): # Only add class if not obsolete.
				fb_feature.addClass(fb['fbid'])
				tmp = re.sub("<up\>", "[",fb['uc_name'])
				uc_name = re.sub("<\/up>", "]", tmp)
				fb_feature.label(fb['fbid'], uc_name)
				if re.match('FBtp\d+', fb['fbid']):
					fb_feature.subClassOf(fb['fbid'], 'SO_0000796')
				elif re.match('FBti\d+', fb['fbid']):
					fb_feature.subClassOf(fb['fbid'], 'SO_0001218')
				elif re.match('FBgn\d+', fb['fbid']):
					fb_feature.subClassOf(fb['fbid'], 'SO_0000704')
				elif re.match('FBal\d+', fb['fbid']):
					fb_feature.subClassOf(fb['fbid'], 'SO_0001023')
				else:
					warnings.warn("Ignoring this, as doesn't look like an FB feature: %s."  % fb['fbid'])
					continue


	time.sleep(0.1)

# vfb_ms_conn.close()

fb_cursor.close()
fb_pg_conn.close()

fb_feature.save("../../owl/fb_features.owl") # yuk
fb_feature.sleep()

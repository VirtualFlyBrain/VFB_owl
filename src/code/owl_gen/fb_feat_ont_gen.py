#!/usr/bin/env jython

import sys
sys.path.append('../mod') # Assuming whole repo, or at least branch under 'code', is checked out, this allows local mods to be found.
from com.ziclix.python.sql import zxJDBC # DB connection
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain
import lmb_fc_tools
import re
import warnings


fbf = "http://purl.obolibrary.org/fbbt/fbfeat/fb_features.owl"
fbf_base = "http://flybase.org/reports/"
fb_feature = Brain(fbf_base, fbf)
# declaration of tmp classes for transgenes
fb_feature.addClass("F73F6684-1B7F-4464-9A3E-6DAB89827C03")
fb_feature.label("F73F6684-1B7F-4464-9A3E-6DAB89827C03", "transposable_element_insertion_site")
fb_feature.addClass("E3091C3F-964B-4C39-8AD3-067221C55442")
fb_feature.label("E3091C3F-964B-4C39-8AD3-067221C55442", "transgenic_transposon")

vfb_ms_conn = lmb_fc_tools.get_con(sys.argv[1], sys.argv[2])
fb_pg_conn = zxJDBC.connect("jdbc:postgresql://flybase.org/flybase", "flybase", "flybase", "org.postgresql.Driver")  #conn to FB pg
vfb_cursor = vfb_ms_conn.cursor()
fb_cursor = fb_pg_conn.cursor()

vfb_cursor.execute("SELECT oc.shortFormID FROM owl_class oc JOIN ontology o ON (oc.ontology_id=oc.ontology_id) WHERE o.URI = '%s'" % (fbf))

flist = []
dc = dict_cursor(vfb_cursor)
for d in dc:
	flist.append(d['shortFormID'])

class_list_string = ''
while flist:
	claz = flist.pop()
	class_list_string += "'%s'" % claz
	if len(flist) >= 1:
		class_list_string += ", "
	
fb_cursor.execute("SELECT f.uniquename AS fbid, synonym_sgml AS uc_name, f.is_obsolete as obstat " \
"FROM synonym s " \
"JOIN cvterm typ ON (typ.cvterm_id=s.type_id) " \
"JOIN feature_synonym fs ON (fs.synonym_id=s.synonym_id) " \
"JOIN feature f ON (f.feature_id=fs.feature_id) " \
"WHERE f.uniquename in (%s) and fs.is_current IS TRUE" % (class_list_string))  # 

fb_dc = dict_cursor(fb_cursor)
for fb in fb_dc:
	if fb['obstat']:
		warnings.warn(fb['fbid'] +" " + fb['uc_name'] + " is obsolete !  Not adding to fb_feature.owl.") 
	else:
		if not fb_feature.knowsClass(fb['fbid']): # Only add class if not obsolete.
			fb_feature.addClass(fb['fbid'])
		tmp = re.sub("<up\>", "[",fb['uc_name'])
		uc_name = re.sub("<\/up>", "]", tmp)
		fb_feature.label(fb['fbid'], uc_name)
		#		fb_feature.subClassOf(fb['fbid'], ??)

vfb_cursor.close()
vfb_ms_conn.close()

fb_cursor.close()
fb_pg_conn.close()

fb_feature.save("../../owl/fb_features.owl") 

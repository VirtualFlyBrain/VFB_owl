from uk.ac.ebi.brain.core import Brain
import sys
# How to get bolt connection?
from neo4j_tools import neo4j_connect
import requests

""" Merges all classes in some specified list of ontologies to neo4J - using short_form
    Adds label (just for reference) and  is_obsolete: T/F
    Arg 1 = ontology access method: 'path' or 'url';
    Arg 2 = usr
    Arg 3 = pwd"""

b = Brain()
nc = neo4j_connect("http://localhost:7474", sys.argv[2],sys.argv[3] )

#TODO - turn this datastruc into a separate config file.

onts_2_learn = { 'fbbi': 
                { 'url': 'http://purl.obolibrary.org/obo/fbbi.owl', 
                 'path': '/repos/fbbi/releases/fbbi-simple.owl'},
                'fbext': 
                { 'url': 'http://purl.obolibrary.org/obo/fbbt/vfb/vfb_ext.owl', 
                 'path': '/repos/VFB_owl/src/owl/vfb_ext.owl'},
                'fbbt': 
                { 'url' : 'http://purl.obolibrary.org/obo/fbbt/fbbt-simple.owl',
                  'path': '/repos/drosophila-anatomy-developmental-ontology/fbbt/releases/fbbt-simple.owl'
                },
                'fb_feature' :
                { 'url' : 'http://purl.obolibrary.org/obo/fbbt/vfb/fb_features.owl',
                  'path' : '/repos/VFB_owl/src/owl/fb_features.owl'
                }
}               

## Switch to owl_pdm_tools to deal with obsoletes?
for k, v in onts_2_learn.items():
    b.learn(v[sys.argv[1]])
    
    
# Get all classes

sc = b.getSubClasses('Thing', 0)

# set constraints

# Add nodes

statements = []
for c in sc:
    label = ''
    try:
        label = b.getLabel(c)
        label = re.sub("'", "\\'", label)
    except:
        pass
    is_obsolete = False
    try:
        if b.getAnnotation(c, 'deprecated') == 'true':
            is_obsolete = True
    except:
        pass
    statements.append('MERGE (c:Class { short_form : "%s")' % c)
    statements.append('MATCH (c:Class { short_form : "%s") SET c.label = "%s" SET c.is_obsolete = %r' 
                      % (c, label, is_obsolete))
        
nc.commit_list(statements)
b.sleep()

from lmb_fc_tools import get_con, owlDbOnt
from uk.ac.ebi.brain.core import Brain
from tsv2pdm import tab
import sys

sys.path.append("../mod/")
con = get_con(usr = sys.argv[1] , pwd = sys.argv[2])  # connection to LMB DB. Need to make ssh tunnel first.

ontologies = Brain() # Construct Brain object

# Now load up ontologies.  These are used to check validity for addition of new classes or 
# relations to DB. You can load as many as you need.
ontologies.learn("http://purl.obolibrary.org/obo/fbbt/fbbt-simple.owl") # Better to use version URI

odbo = owlDbOnt(conn = con, ont = ontologies) # Object for interacting with the database + ontologies.
# Also detects anything that looks like a FlyBase feature and checks validity against public FlyBase.

annotation_table = tab(path = 'data/', file_name='annotations.tsv')

ID_range_start = 20000
for row in annotation_table.tab:
    new_ind = odbo.add_ind(name = row['ind_name'], source = row['ind_source'], ID_range_start = 20000)
    odbo.add_ind_type(ind = new_ind, OWLclass = row['class'], objectProperty = row['rel'])

# Now make an OWL file for source to check new additions.  
# Would be good to roll this into script, but needs to be packaged up a bit better
# For now, can just do a single run of 
# src/code/owl_gen/vfb_ind_runner.py $USR $PD $SOURCE $FBBT, where $FBBT = URL of FBBT to use.
# But should be able to package effectively by slightly refactoring runner script - packaging as class.
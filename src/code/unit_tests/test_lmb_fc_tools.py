from lmb_fc_tools import get_con, owlDbOnt
from uk.ac.ebi.brain.core import Brain
from dict_cursor import dict_cursor
import sys
import warnings

# TODO - switch to standard test framework.
# Switch from warnings to exception catching.

# Better abstraction: Standard test structure - could all be instances of a test class:
# 1. SQL command
# 2. SQL test query
# 3. warning
# 4. cleanup
# 5. return value

# More constraints - add uniqueness constraint on individual labels.

def __main__():
    test = test_suite(sys.argv[1], sys.argv[2], sys.argv[3:])
    return test.run_tests()
    
class test_suite():
    
    # Tests to add: add_owl_entity_2_db
    
    
    def __init__(self, usr,pwd, ont_uri_list):
        self.conn = get_con(usr,pwd)
        self.ont = Brain()
        for uri in ont_uri_list:    
                self.ont.learn(uri)
        self.od = owlDbOnt(self.conn, self.ont)
        self.cleanup_list = []
        
    def run_tests(self):
        self.add_ind_type_test()
        self.add_akv_type_test()
        self.cleanup()
        self.ont.sleep()
        self.conn.close()
  
    
    def add_ind_type_test(self):
        """Combined test of add ind and add_ind_type
        """
        # add ind_test
        self.od.add_ind("add_ind_test", 'CostaJefferis')
        cursor = self.conn.cursor()
        cursor.execute("SELECT * from owl_individual WHERE label = 'add_ind_test'")
        dc = dict_cursor(cursor)
        iid = False
        for d in dc:
            if d['label'] == "add_ind_test": 
                iid = d['id']
            else:
                warnings.warn("Failed to add test ind")
        cursor.close()
        # add ind_type_test
        if iid:
            self.od.add_ind_type(iid, 'BFO_0000050', 'FBbt_00003624')
            typ = self.od.type_exists('BFO_0000050', 'FBbt_00003624')
            stat = False
            if not typ: 
                warnings.warn("Failed to create test type statement")
            else:
                stat = True
        self.cleanup_list.append("DELETE FROM individual_type WHERE id = %s" % typ)  # This must be deleted first.
        self.cleanup_list.append("DELETE from owl_individual WHERE label = 'add_ind_test'")
        return stat
                
    def add_akv_type_test(self):
        self.od.add_akv_type('process', 'note', 'BFO_0000050', 'FBbt_00003624')
        cursor = self.conn.cursor()
        cursor.execute("SELECT at.id FROM annotation_type at " \
                       "JOIN annotation_key_value akv ON (akv.id = at.annotation_key_value_id) " \
                       "JOIN owl_type ot ON (ot.id=at.owl_type_id)")
        dc = dict_cursor(cursor)
        ID = ''
        for d in dc:
            ID = d['id']
        if not ID:
            warnings.warn("Failed to add akv type.")
        self.cleanup_list.append("DELETE FROM annotation_type WHERE id = %s" % ID)
        return ID
    
    def cleanup(self):
        cursor = self.conn.cursor()
        for command in self.cleanup_list:
            cursor.execute(command)  
        self.conn.commit()

        
__main__()

    



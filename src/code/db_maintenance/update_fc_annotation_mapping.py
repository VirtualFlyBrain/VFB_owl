from lmb_fc_tools import owlDbOnt
from lmb_fc_tools import get_con
from uk.ac.ebi.brain.core import Brain
from tsv2pdm import tab, compare_tabs
import sys
import warnings
        
def gen_report_tab(od):
    headers = ['a.annotation_type', 'a.text', 'op_label', 'op_id', 'class_label', 'class_id']  # Doesn't seem right to set this here...
    report = tab(headers = headers)
    dc = od.gen_annotation_report()
    for d in dc:
        row = {}
        row['a.annotation_type'] = d['annotation_class']
        row['a.text'] = d['annotation_text']
        row['op_label'] = d['op_label']
        row['op_id'] = d['op_id']
        row['class_label'] = d['class_label'] 
        row['class_id'] = d['class_id']
        report.tab.append(row)
    return report

        
def update_akv_from_tab(od, table, safe_mode = True):
    """
    Updates mappings in the DB as specified in a mapping table (tsv).
    od = owlDbOnt, table = updated mapping table (as tab object); 
    If safe mode = True (default), missing mappings are not deleted.  
    If it is set to false, they are."""    
    # Should probably move all out this out
    # For ref
    # headers = ['a.annotation_type', 'a.text', 'op_label', 'op_id', 'class_label', 'class_id'] # Feels wrong to hard-wire here.
    
    # Mappings currently in DB
    report = gen_report_tab(od)
    # All mappings specified in update table
    update = table
    
    ct = compare_tabs(tab1 = report, tab2 = update) # Takes care of header checks
    
    # Only in the report tab
    deleted = ct.tab1_only()
    # Only in the update tab
    new = ct.tab2_only()
    for r in new.tab:
        warnings.warn("Processes %s" % r)
        if r['class_id']:
            od.add_akv_type(key = r['a.annotation_type'], value =r['a.text'] , OWLclass = r['class_id'], objectProperty =r['op_id'] )
    else:
        for r in deleted.tab:
            if not safe_mode:
                od.remove_akv_type(key = r['a.annotation_type'], value =r['a.text'] , OWLclass = r['class_id'], objectProperty =r['op_id'] )     
            else:
                warnings.warn("Row present in DB, now missing from mapping: %s. %s.  " \
                              "Safe mode set so not deleting" % (r['a.annotation_type'], r['a.text']))

c = get_con(sys.argv[1], sys.argv[2])
b = Brain()
b.learn(sys.argv[3]) # Path to ontology file with referenced terms (presumably fbbt_simple will suffice) 
od = owlDbOnt(conn = c, ont = b)
update_table = tab("../../../doc/", "annotation_map.tsv")
update_akv_from_tab(od, update_table) # Assumes update table has all mappings. If it lacks any, assumes these mappings are to be deleted!  This is potentially dangerous if mapping table is out of sync with DB.
outfile = open("../../../doc/annotation_map_report.tsv", "w")  
report_tab = gen_report_tab(od)
outfile.write(report_tab.print_tab(sort_keys = ('a.annotation_type', 'a.text')))
outfile.close()


c.commit()
c.close()
b.sleep()

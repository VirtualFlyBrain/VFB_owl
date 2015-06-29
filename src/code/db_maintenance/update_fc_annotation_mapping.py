from lmb_fc_tools import owlDbOnt
from lmb_fc_tools import get_con
from uk.ac.ebi.brain.core import Brain
from tsv2pdm import tab, compare_tabs
import sys








        
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
    return report_tab
        
def update_akv_from_tab(od, table):
    # Should probably move all out this out
    # For ref
    # headers = ['a.annotation_type', 'a.text', 'op_label', 'op_id', 'class_label', 'class_id'] # Feels wrong to hard-wire here.
    report = gen_report_tab
    update = table.tab
    ct = compare_tabs(tab1 = report, tab2 = update) # Takes care of header checks
    deleted = ct.tab1only().tab
    new = ct.tab2only().tab
    for r in new():
        od.add_akv_type(key = r['annotation_type'], value =r['a.text'] , OWLclass = r['class_id'], objectProperty =r['op_id'] )     
    for r in deleted:
        od.remove_akv_type(key = r['annotation_type'], value =r['a.text'] , OWLclass = r['class_id'], objectProperty =r['op_id'] )     

c = get_con(sys.argv[1], sys.argv[2])
b = Brain()
b.learn("http://purl.obolibrary.org/obo/fbbt/fbbt-simple.owl") 
od = owlDbOnt(conn = c, ont = b)
update_table = tab("mapping_tables/", "annotation_map.tsv")
update_akv_from_tab(od, update_table)
outfile = open("mapping_tables/annotation_map_report.tsv")  
report_tab = gen_report_tab(od)
outfile.write(report_tab.print_tab(sort_keys = ('a.annotation_type', 'a.text')))


c.commit()
c.close()
b.sleep()

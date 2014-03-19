#!/usr/bin/env Jython
import sys
sys.path.append('../src/code/mod')
from dict_cursor import dict_cursor
from lmb_fc_tools import get_con

con = get_con(sys.argv[1], sys.argv[2])

cursor = con.cursor()
cursor.execute("SELECT akv.annotation_class, akv.annotation_text, op.label AS op_label, op.shortFormID AS op_id, oc.label AS class_label, oc.shortFormID AS class_id " \
"FROM annotation_key_value akv " \
"LEFT OUTER JOIN annotation_type  at ON (akv.id = at.annotation_key_value_id) " \
"LEFT OUTER JOIN owl_type t ON at.owl_type_id = t.id " \
"LEFT OUTER JOIN owl_class oc ON t.class = oc.id " \
"LEFT OUTER JOIN owl_objectProperty op ON t.objectProperty = op.id " \
"WHERE annotation_class IN ('NeuronType', 'MainTract', 'ALGlomerulus', 'NeuronSubType', 'laterality', 'ImageType') " \
"ORDER BY annotation_class")

dc = dict_cursor(cursor)

FH = open("annotation_map.md", 'w')
FH.write("| a.annotation_type | a.text | op_label | op_id | class_label | class_id |\n|---|---|---|---|---|---|\n")

for d in dc:
    FH.write("| %s | %s | %s | %s | %s | %s |\n" % (d['annotation_class'], d['annotation_text'], d['op_label'], d['op_id'], d['class_label'], d['class_id']))

FH.close()
cursor.close()
con.close()

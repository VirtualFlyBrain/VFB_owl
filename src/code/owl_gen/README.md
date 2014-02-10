# Generating OWL files:

From src/code/owl_gen/:

 * generate fb_features ontology: ./fb_feat_ont_gen.py usr pwd
 *  generate flycircuit individuals:  ./fc_ind.py usr pwd
 *  generate any other dataset individuals:  ./vfb_ind_runner.py usr pwd dataset
  * where dataset = flycircuit.data_source.name

Output files are hard coded.  Run from src/code/owl_gen/ for them to end up in src/owl/ .

To avoid this, use vfb_ind_tools.gen_ind_by_source directly.

# Generating OWL files:

From src/code/owl_gen/:

 * generate fb_features ontology: ./fb_feat_ont_gen.py usr pwd
 *  generate flycircuit individuals:  ./fc_ind.py usr pwd
 *  generate any other dataset individuals:  ./vfb_ind_runner.py usr pwd dataset
  * where dataset = flycircuit.data_source.name

Output file names and paths are hard coded.  Run from src/code/owl\_gen/ for them to end up in src/owl/. To avoid this, use vfb\_ind\_tools.gen\_ind\_by\_source directly.

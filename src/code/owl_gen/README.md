# Generating OWL files:

From src/code/owl_gen/:

 * generate fb_features ontology: ./fb_feat_ont_gen.py usr pwd
 *  generate flycircuit individuals:  ./fc_ind.py usr pwd
 *  generate any other dataset individuals:  ./vfb_ind_runner.py usr pwd dataset
  * where dataset = flycircuit.data_source.name *

Output file names and paths are hard coded into vfb\_ind\_runner.py to conform to the standard release pipeline nomenclature and file locations. This should be run from src/code/owl\_gen/ in a complete checkout of thr repo for them to end up in src/owl/. To choose your own file names and paths please use gen\_ind\_by\_source.py directly, specifying a source name*. 

\* source name must be an entry flycircuit.data_source.name.  Current sources:

    +--------------------+-------------------------------+----------+
    | name               | pub_miniref                   | pub_pmid |
    +--------------------+-------------------------------+----------+
    | Yu2013             | Yu et al., 2013               | 23541733 |
    | Ito2013            | Ito et al., 2013              | 23541729 |
    | Cachero2010        | Cachero et al., 2010          |          |
    | Knowles-Barley2010 | Knowles-Barley et al., 2010   |          |
    | Jenett2012         | Jenett et al., 2012           | 23063364 |


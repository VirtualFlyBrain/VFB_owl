from uk.ac.ebi.brain.core import Brain
from owl2pdm_tools import typeAxioms2pdm
import  json

# A rather Perlish datastructure.  The result of writing to JSON as an intermediate.
# TODO: add field to record general classification - either via extension to Brain, or a cruder Python look


def gen_pdm_from_indfile(ont_url, outfile):
    """Reads an owl file from ont_url; Writes a JSON file (outfile) of 
    types and annotations on individuals in the file.
    JSON structure: 
    id: 
       label: string
       def: string
       types:
         - isAnonymous:boolean; 
         - relId:URI_string; 
         - objectId:URI_string.
    """
    
    ont = Brain()
    ont.learn(ont_url)
    onto = ont.getOntology()    
    inds = ont.getInstances("Thing", 0)
    axioms = {}
    
    for i in inds:
        axioms[i] = {}
        axioms[i]["Types"] = typeAxioms2pdm("http://www.virtualflybrain.org/owl/" + i, onto) # Hard wired baseURI - should pass!
        axioms[i]["label"] = ont.getLabel(i)
        axioms[i]["def"] =  ont.getAnnotation(i, "IAO_0000115")
        
        # Need boolean checks.  Not sure Brain can do this for individuals, if not - can do slow, iterative check
        # if (is expression pattern):
        # axioms[i]["general_classification"] = "expression pattern"
        # elif (is neuron)
        # axioms[i]["general_classification"] = "neuron"
        # if (is clone)
        # axioms[i]["general_classification"] = "clone"

    jfile = open(outfile, "w")
    jfile.write(json.dumps(axioms, sort_keys=True, indent=4))
    ont.sleep()
    

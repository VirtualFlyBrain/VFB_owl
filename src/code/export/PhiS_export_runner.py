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
    axioms = {}

    
    def gen_pdm(ont, inds, classification):   
        axioms = {} 
        for i in inds:
            axioms[i] = {}
            axioms[i]["Types"] = typeAxioms2pdm("http://www.virtualflybrain.org/owl/" + i, onto) # Hard wired baseURI - should pass!
            axioms[i]["label"] = ont.getLabel(i)
            axioms[i]["def"] =  ont.getAnnotation(i, "IAO_0000115")
            axioms[i]["general_classification"] = classification            
        return axioms
   
    axioms.update(gen_pdm(ont.getInstances("B8C6934B-C27C-4528-BE59-E75F5B9F61B6", 0), "B8C6934B-C27C-4528-BE59-E75F5B9F61B6")) # expression_patterns
    axioms.update(gen_pdm(ont.getInstances("FBbt_00005106", 0), "FBbt_00005106")) # neurons
    axioms.update(gen_pdm(ont.getInstances("FBbt_00007683", 0), "FBbt_00007683")) # clones
    jfile = open(outfile, "w")
    jfile.write(json.dumps(axioms, sort_keys=True, indent=4))
    ont.sleep()
        

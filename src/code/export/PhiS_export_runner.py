from uk.ac.ebi.brain.core import Brain
from owl2pdm_tools import ont_manager
import  json


ont_url = ''
outfile = ''

def gen_pdm(ont, inds, classification):   
    axioms = {}
    om = ont_manager(ont.getOntology())  
    for i in inds:
        axioms[i] = {}
        axioms[i]["Types"] = om.typeAxioms2pdm(sfid = i)
        axioms[i]["label"] = ont.getLabel(i)
        axioms[i]["def"] =  ont.getAnnotation(i, "IAO_0000115")
        axioms[i]["general_classification"] = classification            
    return axioms


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
    axioms = {}
    if ont.knowsClass("B8C6934B-C27C-4528-BE59-E75F5B9F61B6"):
        axioms.update(gen_pdm(ont, ont.getInstances("B8C6934B-C27C-4528-BE59-E75F5B9F61B6", 0), "B8C6934B-C27C-4528-BE59-E75F5B9F61B6")) # expression_patterns
    if ont.knowsClass("FBbt_00005106"):
        axioms.update(gen_pdm(ont, ont.getInstances("FBbt_00005106", 0), "FBbt_00005106")) # neurons
    if ont.knowsClass("FBbt_00007683"):
        axioms.update(gen_pdm(ont, ont.getInstances("FBbt_00007683", 0), "FBbt_00007683")) # clones
    jfile = open(outfile, "w")
    jfile.write(json.dumps(axioms, sort_keys=True, indent=4))
    ont.sleep()
        

def __main__():
    datasets = ['Cachero2010', 'Ito2013', 'Yu2013', 'Jenett2012_full', 'flycircuit_plus']
    #base = 'http://purl.obolibrary.org/obo/fbbt/vfb/'
    base = 'file:///repos/VFB_owl/src/owl/'
    for d in datasets:
        gen_pdm_from_indfile(ont_url = base + d + ".owl", outfile = d + ".json")
        
__main__()
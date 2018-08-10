'''
Created on May 21, 2018

@author: matentzn
'''

import urllib as ul
import json 

#Gepetto docs are documented here: https://github.com/matentzn/ontologies/blob/master/GepettoDependencies.md

def callowlery(query,sbcl=True, verbose=False):
    owlery="http://owl.virtualflybrain.org/kbs/vfb/"
    q='subclasses?object='+query+'&direct=false'
    nothing = 'http://www.w3.org/2002/07/owl#Nothing'
    index='superClassOf'
    if sbcl==False:
        q='instances?object='+query+'&direct=false'
        index='hasInstance'    
    res=set(parseJSON(owlery+q,verbose)[index])
    if nothing in res:
        res.remove(nothing)
    return set(res)

def callaberowl(query,sbcl=True, verbose=False):
    aberowl="http://owl.virtualflybrain.org/api/runQuery.groovy?"
    q='type=subeq&query='+query+'&ontology=VFB'
    if sbcl==False:
        q='type=realize&query='+query+'&ontology=VFB'
    res=parseJSON(aberowl+q,verbose)
    out = list()
    res['result']
    for l in res['result']:
        out.append(l['classURI'])
    return set(out)

def parseJSON(resturl,verbose=False):
    print(resturl)
    with ul.request.urlopen(resturl) as url:
        data = json.loads(url.read().decode())
        return data
    
def test(query, sbcl=True, verbose=False):
    res_a=callaberowl(query,sbcl,verbose)
    res_o=callowlery(query,sbcl,verbose)
    if verbose==True:
        print('*AberOWL*')
        print(res_a)
        print('*OWLERY*')
        print(res_o)
        print('*AberOWL not OWLERY*')
        print(res_a - res_o)
        print('*OWLERY not AberOWL*')
        print(res_o - res_a)
    return(set(res_a) == set(res_o))

def uc(s):
    return ul.parse.quote_plus(s)

# owlery does not allow THAT
# aberowl returns self in subclass query es subset eq.!
# owlery returns obsolete classes http://purl.obolibrary.org/obo/FBbt_00002047

#SUBCLASS
def run_tests(ID,verbose=False):
    ID='FBbt_00007239'
    description="Part of"
    partof=uc('<http://purl.obolibrary.org/obo/BFO_0000050> some <http://purl.obolibrary.org/obo/'+ID+'>')
    print(test(partof,verbose=verbose))
    
    description="Neurons with some part here"
    neu_part=uc('<http://purl.obolibrary.org/obo/FBbt_00005106> and <http://purl.obolibrary.org/obo/RO_0002131> some <http://purl.obolibrary.org/obo/'+ID+'>')
    print(test(neu_part,verbose=verbose))
    
    ID='FBbt_00007054'
    description="Neurons with synaptic terminals here"
    neu_synterm=uc('<http://purl.obolibrary.org/obo/FBbt_00005106> and <http://purl.obolibrary.org/obo/RO_0002130> some <http://purl.obolibrary.org/obo/'+ID+'>')
    print(test(neu_synterm,verbose=verbose))
    
    description="Neurons with presynaptic terminals here"
    neu_presynterm=uc('<http://purl.obolibrary.org/obo/FBbt_00005106> and <http://purl.obolibrary.org/obo/RO_0002113> some <http://purl.obolibrary.org/obo/'+ID+'>')
    print(test(neu_presynterm,verbose=verbose))
    
    description="Neurons with postsynaptic terminals here"
    neu_postsynterm=uc('<http://purl.obolibrary.org/obo/FBbt_00005106> and <http://purl.obolibrary.org/obo/RO_0002110> some <http://purl.obolibrary.org/obo/'+ID+'>')
    print(test(neu_postsynterm,verbose=verbose))
    
    ID='FBbt_00002037'
    description="Neuron classes fasciculating here"
    neu_fasc=uc('<http://purl.obolibrary.org/obo/FBbt_00005106> and <http://purl.obolibrary.org/obo/RO_0002101> some <http://purl.obolibrary.org/obo/'+ID+'>')
    print(test(neu_fasc,verbose=verbose))
    
    ID='FBbt_00014013'
    description="tracts in"
    tractsin=uc('<http://purl.obolibrary.org/obo/FBbt_00005099> and <http://purl.obolibrary.org/obo/RO_0002134> some <http://purl.obolibrary.org/obo/'+ID+'>')
    print(test(tractsin,verbose=verbose))
    
    description="Subclasses of"
    subclass=uc('<http://purl.obolibrary.org/obo/'+ID+'>')
    print(test(subclass,verbose=verbose))
    
    ID='FBbt_00007401'
    description="Lineage clones found in"
    lineageclones=uc('<http://purl.obolibrary.org/obo/FBbt_00007683> and <http://purl.obolibrary.org/obo/RO_0002131> some <http://purl.obolibrary.org/obo/'+ID+'>')
    print(test(lineageclones,verbose=verbose))
    
    # REALISE
    ID='FBbt_00007054'
    description="Images of neurons with some part here (clustered)"
    img_part=uc('<http://purl.obolibrary.org/obo/C888C3DB-AEFA-447F-BD4C-858DFE33DBE7> some ( <http://purl.obolibrary.org/obo/FBbt_00005106> and <http://purl.obolibrary.org/obo/RO_0002131> some <http://purl.obolibrary.org/obo/'+ID+'>)')
    print(test(img_part,sbcl=False,verbose=verbose))
    
    description="Images of neurons with some part here"
    img_neupart=uc('<http://purl.obolibrary.org/obo/FBbt_00005106> and <http://purl.obolibrary.org/obo/RO_0002131> some <http://purl.obolibrary.org/obo/'+ID+'>') # 
    print(test(img_neupart,sbcl=False,verbose=verbose))

run_tests(ID='FBbt_00007239',verbose=True)

ID='FFBbt_00003624'

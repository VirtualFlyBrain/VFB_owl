#!/usr/bin/env jython

import warnings

    
def addOboAnnotationProperties(brain):
    """Add obo annotation property declarations to a brain object"""
    brain.addAnnotationProperty("http://purl.obolibrary.org/obo/IAO_0000115") # definition
    brain.addAnnotationProperty("http://purl.obolibrary.org/obo/IAO_xref") # ??
    brain.addAnnotationProperty("http://www.geneontology.org/formats/oboInOwl#hasExactSynonym")
    brain.addAnnotationProperty("http://www.geneontology.org/formats/oboInOwl#hasBroadSynonym")
    brain.addAnnotationProperty("http://www.geneontology.org/formats/oboInOwl#hasNarrowSynonym")
    brain.addAnnotationProperty("http://www.geneontology.org/formats/oboInOwl#hasRelatedSynonym")
    brain.addAnnotationProperty("http://www.geneontology.org/formats/oboInOwl#hasDbXref")
    return brain

def addVFBAnnotationProperties(brain):
    brain.addAnnotationProperty("http://purl.obolibrary.org/obo/fbbt/vfb/VFBext_0000005") # data_source_link


def gen_id(idp, ID, length, id_name):
    """ARG1: ID prefix (string), ARG 2 starting ID number (int), ARG3, length of numeric portion ID, ARG4 an id:name hash"""
    def gen_key(ID, length):  # This function is limited to the scope of the gen_id function.
        dl = len(str(ID)) # coerce int to string.
        k = idp+'_'+(length - dl)*'0'+str(ID)
        return k
    k = gen_key (ID, length)
    while k in id_name:
        ID += 1
        k = gen_key(ID, length)
    return (k, ID) # useful to return ID to use for next round.

def test_gen_id():

    # make a dict

    id_name = {}
    id_name['HSNT_00000101'] = 'head'
    id_name['HSNT_00000102'] = 'shoulders'
    id_name['HSNT_00000103']= 'knees'

    # Set intial variables

    start = 101
    length = 8
    idp = 'HSNT'

    # Generate new ID
    (k, ID) = gen_id(idp, start, length, id_name)
    if not k == 'HSNT_00000104':
        warnings.warn('gen_id is broken!')

test_gen_id()

#!/usr/bin/env jython

import sys
import warnings
from com.ziclix.python.sql import zxJDBC # DB connection
from dict_cursor import dict_cursor  # Handy local module for turning JBDC cursor output into dicts
from uk.ac.ebi.brain.error import BrainException
from uk.ac.ebi.brain.core import Brain


def entity_check(SFID_list):
    conn = zxJDBC.connect("jdbc:mysql://localhost/flycircuit", sys.argv[1], sys.argv[2], "org.gjt.mm.mysql.Driver")
    cursor = conn.cursor()
    class owl_entity(): # v.simple object for storing attributes of class
        ont = ''
        base = ''
        sfid = ''
        typ = ''
        
    ont_dict = {} # Dict to make a uniq'd list of ontologies
    sfid_oe = {} # Dict of owl_entities - as specified by DB
    for SFID in SFID_list:
        cursor.execute("SELECT DISTINCT ontology_URI AS ont, owl_type as typ, baseURI as base FROM owl_entity WHERE shortFormID = '%s'" % SFID)
        
        dc = dict_cursor(cursor)
        brain = Brain()
        sfo = owl_entity()
        for d in dc:
            ont = d['ont']
            if not ont in ont_dict:
                brain.learn(ont)
                ont_dict[ont] = brain
            sfo.ont = d['ont']
            sfo.base = d['base']
            sfo.typ = d['typ']
            
        sfid_oe[SFID] =  sfo

    for idt in sfid_oe.items():
        SFID = idt[0]
        owlEnt = idt[1]
        ont = owlEnt.ont
        brain = ont_dict[ont]
        #        if brain.getAnnotation(SFID, 'deprecated'): # Need to cope with cases where it is not deprecated!
        #            print SFID + ' is obsolete!' 
        if owlEnt.typ == 'class':
            if not brain.knowsClass(SFID):
                print 'Unknown Class SFID in ' + owlEnt.ont
        elif owlEnt.brain == 'objectProperty':
            if not ont.knowsClass(SFID):
                print 'Unknown objectProperty SFID in ' + owlEnt.ont
    
                #def oc_check():
    

            
test_list = ('FBbt_00003983', 'FBbt_00007482', 'FBbt_00003985')
entity_check(test_list)
            



#!/usr/bin/env jython
import warnings

def def_roller(types, ont):
	"""Take a list of simple owl class expression objects (soce) as an arg. Each soce has 2 attributes - a relation (rel) and an object (obj).  The value of each attribute is a shortFormID"""
	genus = ''
	po = ''
	exp = ''
	defn = ''
	gender = ''
	for typ in types:
		if not typ.rel:
			if typ.obj == 'FBbt_00005106': # neuron
				genus = 'neuron'
			elif typ.obj == 'B8C6934B-C27C-4528-BE59-E75F5B9F61B6': # expression pattern
				genus = 'expression pattern'
			elif typ.obj == 'FBbt_00007683': # neuroblast lineage clone
				genus = 'neuroblast lineage clone'
		if (typ.rel == 'BFO_0000050') & (typ.obj == 'FBbt_00003624'): # part of adult brain
			po = 'adult brain'
		if (typ.rel == 'BFO_0000050') & (typ.obj == 'FBbt_00007004'): # part male organism
				gender = 'M'
		if (typ.rel == 'BFO_0000050') & (typ.obj == 'FBbt_00007011'): # part female organism
				gender = 'F'
		if (typ.rel == 'RO_0002292'): # expresses  X
			exp = ont.getLabel(typ.obj)
	if gender == 'M':
		po = 'adult male brain'
	if gender == 'F':
		po = 'adult female brain'
	if genus == 'neuron':
		defn = "A neuron expressing %s that is part of an %s." % (exp, po)
	elif genus == 'expression pattern':
		defn = "An %s expressing %s" % (po, exp)
	elif genus == 'neuroblast lineage clone':
		defn = "An example of an %s in the %po." % (genus, po)
	return defn

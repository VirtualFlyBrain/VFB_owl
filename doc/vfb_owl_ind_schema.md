## VFB schema for representing individual anatomical structures as OWL individuals

[Note - using labels in place of URIs for readability]

	
    Individual: 'cluster A'
        has_exemplar: 'ind X'
    Individual: 'ind X'
        Types:
     	    neuron
     	    part_of some 'adult brain'
     	    overlaps some 'fan-shaped body'
     	    overlaps some nodulus
            releases_neurotransmitter some dopamine
        Facts:
            exemplar_of 'cluster A'  # can be inferred via inverse if using full DL reasoner

    Individual: 'ind Y'
        Types:
            neuron
     	    part_of some 'adult brain'
    	    overlaps some 'fan-shaped body'
     	    overlaps some nodulus
        Facts:
     	    member_of: 'cluster A'

    ObjectProperty: member_of

    ObjectProperty: exemplar_of
        SubObjectPropertyOf: member_of

    ObjectProperty: has_exemplar
        InverseOf: exemplar_of

    Individual: 'lineage clone Z'
        Type: <some lineage clone>


For query purposes, the individuals file is combined with the full version of the Drosophila anatomy ontology and a file of direct assertions of neuron type.  The full version is necessary as there is some inference based on equivalent class assertions.

For analysis purposes, it can also combined with an individuals file of images with the schema:

    Individual: <URL of thumbnail image>
        Types:
            foaf:image
        Facts:
            foaf:depicts 'ind A'


This Schema for images => compatibility with [this Protege image viewer plugin](https://github.com/balhoff/image-depictions-view).
# Documentation for the json tree files used on VFB

## Background 

The javascript that drives the clickable tree on VFB is derived from the defunct [mif-tree](https://github.com/creaven/miftree) library.
In the absence of any official spec for these json files, the spec here is reverse engineered.  If you know of any official spec, please let us know.

## Details

Each tree is driven by two files: treeStructure.jso encodes the structure of the tree,  treeContent.jso encodes information about each node in the tree, including name, color, anatomy ontology class ID and an ID for the domain on the image stack.

### Interaction between trees

Bizarrely, it is not sufficient for treeContent.jso to have nodeIds that match all of the nodes in treeStructure.jso. The order in the treeContent array has to be the same as the order of nodes in treeStucture.jso AND the nodeId numbering need to be consecutive (no gaps). (I haven't yet test whether they need to start from zero.)




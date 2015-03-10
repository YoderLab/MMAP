# MMAP: Microbial Metagenomic Analysis Pipeline

Developing a software package to analysis metagenomics data

Language: Python 2.7
Required package
* Biopython - 1.64
* NumPy - 1.8.2
* SciPy - 0.12.1

Required software
* **Genovo** v0.4: http://cs.stanford.edu/group/genovo/
* **Glimmer** v3.02: https://ccb.jhu.edu/software/glimmer/
  * requires **ELPH** v1.0.1:  http://cbcb.umd.edu/software/ELPH/
* **MINE.jar** v1.0.1: http://www.exploredata.net/
* **NCBI BLAST+** v2.2.28+: http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download

Note: These software distributed here might not work with your OS!  

## INSTALL

### Directory list
Default/Recommended folder structure. 
This structure is used in default control file. If Genovo/Glimmer/MINE/BLAST are located at other destination, please update the control file.
* data
 * example ## contain a basic example
 * Genovo
 * Glimmer
 * MINE
 * BLAST # Contains `blastx`, which is a symlink to `/usr/bin/blastx`
* src
 * core 
 * test

### Generate local blast database

The BLAST component is designed to query the Gene Ontology sequences from http://geneontology.org. Prior to running, you must create a local BLAST+ formatted database and include its path in the control file

## USAGE

```
#edit the control file "data/example/control"; Update "parent_directory=" and point that to the data/ directory 
cd MMAP;
python src/core/main.py data/example/control
```


### Directory list
* data
 * example - testing dataset
* src - source code
 * core 
 * test - use unittest in Python


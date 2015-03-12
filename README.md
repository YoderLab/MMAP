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

### Generating local blast database

The BLAST component queries annotated Gene Ontology sequences downloaded from http://geneontology.org. Prior to running an analysis, you must download the sequences and convert them to a BLAST+ formatted database.

A bash script is provided that does this automatically: [src/scripts/makeblastdb-go.sh]. It uses [curl](http://curl.haxx.se) and [makeblastdb](http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) to download a FASTA-formatted protein sequence and convert it to NCBI BLAST+ format.

It accepts one argument - the output directory for the GO Sequence Database.

    $ ./makeblastdb-go.sh /data/go-seqdb

After generating the local database, add its path to the control file, so that the pipeline knows where to find it.

## USAGE

```
#edit the control file "data/example/control"; Update "parent_directory=" and point that to the data/ directory. Update "go_blastdb=" to point to the converted BLAST DB directory
cd MMAP;
python src/core/main.py data/example/control
```


### Directory list
* data
 * example - testing dataset
* scripts - utilities
* src - source code
 * core 
 * test - use unittest in Python


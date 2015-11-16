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
* **MINE** v1.0.1: http://www.exploredata.net/
  * requires **Java**: http://www.java.com/
* **NCBI BLAST+** v2.2.28+: http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download

Note: Binary files distributed here might **NOT** work with your OS!  

## INSTALL

#### Default directory list
The following folder structure is used in the default control file. If Genovo/Glimmer/MINE are located at other destinations, please update the control file.
* data
 * example ## contain basic examples
 * Genovo
 * Glimmer
 * MINE
 * BLAST # Contains `blastx`, which is a symlink to `/usr/bin/blastx`
* src
 * core
 * test

#### Setup control file
  * The control file in MMAP have two purpose. The main purpose is allowing MMAP to locate other software (genovo, glimmer, MINE, and blast).
  * The secondary purpose is to allow users to customize the parameters used in the pipeline. Please refer to the [Additional parameters](Additional-parameters-in-the-control-file) section.


#### Setup Genovo
  1. Genovo shipped with precompiled binaries. Check and run the commented demo script `DEMO.sh`.
  2. If these precompiled binaries or the demo script fail. Recompile it from the `src` folder. The default Makefile requires `libtool`
  3. Update control file accordingly. Make sure `genovo_pdir` points to the folder contains the following binaries `assemble` and `finalize`.

#### Setup Xgenovo
  1. Compile Xgenovo.
  2. Update control file accordingly. Make user 'xgenovo_pdir' points to the folder contains the following binaries `assemble` and `finalize`.
#### Setup Glimmer
  1. Glimmer often required some custom setup. Try to use full/absolute path if relative path doesn't work.
  2. Follow the instruction in `glim302notes.pdf` and compile glimmer from the source code.
  3. Download and install elph
  4. Update `awkpath`, `glimmerpath`, and `elphbin` in  `glimmer/scritps/g3-iterated.csh`
    * The awkpath should be points to the `scritps` folder
    * The glimmerpath should point to the `bin` folder
    * The elphbin is the full path points to the executable `elph`. Not the folder.
  5. Update control file accordingly. Make sure `glimmer_pdir` points to the top level of the glimmer folder. MMAP is looking for `bin` and `scripts` underneath this folder.

#### Generating local blast database

The BLAST component queries annotated Gene Ontology sequences downloaded from http://geneontology.org. Prior to running an analysis, you must download the sequences and convert them to a BLAST+ formatted database.

A bash script is provided that does this automatically: [src/scripts/makeblastdb-go.sh]. It uses [curl](http://curl.haxx.se) and [makeblastdb](http://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=Download) to download a FASTA-formatted protein sequence and convert it to NCBI BLAST+ format.

It accepts one argument - the output directory for the GO Sequence Database.

    $ ./makeblastdb-go.sh /data/go-seqdb

After generating the local database, add its path to the control file, so that the pipeline knows where to find it.

#### Setup MINE
  1. Install and make sure your java version is at least 1.7 (`java -version`)
  2. Update control file accordingly. Make sure `mine_pdir` points to the folder contains `MINE.jar`.


## USAGE

* Update control file [default: MMAP/control]
 * program_pdir points to the directory contains the exe
 * blasd_db pointst to the local BLAST database

```
python MMAP/main.py -h
python MMAP/main.py summary -h
python MMAP/main.py process -h


## To run Genovo/Glimmer/Blast, use -i to provide input fasta file
python MMAP/main.py process -c data/example/control -i data/example/MMAP_example.fasta
python MMAP/main.py process -c data/example/controlX -i data/example/MMAP_paired_example.fasta

## To run MINE, use -m to provide a directory with list of csv files
python MMAP/main.py summary -m data/example/

## Custom control file can be used wit -c
python MMAP/main.py process -i data/example/MMAP_example.fasta -c path_to_custom_control_file
```
### Additional parameters in the control file

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
* **MINE.jar** v1.0.1: http://www.exploredata.net/

Note: These software distributed here might not work with your OS!  


## INSTALL
### Directory list
Default/Recommended folder structure. This structure is used in default control file. If Genovo/Glimmer/MINE are locate at other destination, please update the control file.
* data
 * Genovo
 * Glimmer
 * MINE
* src
 * core 
 * test



## USAGE
```
cd src;
python core/main.py /full_path_to_control_file/control_file
```


### Directory list
* data - testing dataset
* src - source code
 * core 
 * test - use unittest in Python


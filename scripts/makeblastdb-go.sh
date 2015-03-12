#!/bin/bash

if [ -z "$1" ]
then
  BLASTDB="/go-blastdb"
else
  BLASTDB=$1
fi

# Check if a sequence database already exists
if [ -f "$BLASTDB/go-seqdb.pin" ]
then
  echo "Aborting: Sequence database $BLASTDB/go-seqdb already exists"
  exit 1
fi

echo "Making BLASTDB at $BLASTDB"

# Make the directory if it doesn't exist
mkdir -p $BLASTDB

# Download the fasta version of the GO seqdb
GO_SEQDB_URL=http://archive.geneontology.org/lite/2015-02-14/go_20150214-seqdb.fasta.gz
curl -SL -o /tmp/go-seqdb.fasta.gz $GO_SEQDB_URL
gunzip /tmp/go-seqdb.fasta.gz

# Make the database
makeblastdb \
  -in /tmp/go-seqdb.fasta \
  -out $BLASTDB/go-seqdb \
  -dbtype prot \
  -parse_seqids \
  -title go-seqdb

# Cleanup
rm /tmp/go-seqdb.fasta



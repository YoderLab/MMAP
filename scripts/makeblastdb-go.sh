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
#GO_SEQDB_URL_V=http://archive.geneontology.org/lite/latest/go_20150214-seqdb.fasta.gz
GO_SEQDB_URL=http://archive.geneontology.org/lite/latest/
#curl -SL -o /tmp/go-seqdb.fasta.gz $GO_SEQDB_URL
#SEQDB_NAME=`curl --list-only http://archive.geneontology.org/lite/latest/ |  sed -n 's%.*href="\([^.]*seqdb\.fasta\.gz\)".*%\n\1%; ta; b; :a; s%.*\n%%; p'`i
SEQDB_NAME=`curl -n --list-only http://archive.geneontology.org/lite/latest/ | grep -oE  go_[0-9]{8}-seqdb\.fasta\.gz | uniq`
curl -SL -o /tmp/go-seqdb.fasta.gz ${GO_SEQDB_URL}${SEQDB_NAME}
gunzip /tmp/go-seqdb.fasta.gz

# Make the database
makeblastdb \
  -in /tmp/go-seqdb.fasta \
  -out $BLASTDB/go-seqdb \
  -dbtype prot \
  -parse_seqids \
  -title go-seqdb

# Cleanup
#rm /tmp/go-seqdb.fasta



#!/usr/bin/env python

# This script parses the gene ontology IDs out of the titles in a blast result csv file
# It extracts the GO:XXXXX terms from the last column of a CSV file, and counts the instances of each

import csv
import re
import os


def read_terms(input_file_name):
  terms_dict = dict()

  def add_term(terms_dict, term):
    if term not in terms_dict:
      terms_dict[term] = 0
    terms_dict[term] += 1

  with open(input_file_name, 'rb') as csvfile:
    pattern = re.compile("(\[(GO:.*?)\s.*?\])")
    reader = csv.reader(csvfile)
    for row in reader:
      titles = row[-1]
      gos = pattern.findall(titles)
      [add_term(terms_dict, go[1]) for go in gos]

  return terms_dict

def write_terms(terms_dict, output_file_name):
  with open(output_file_name, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["GoTerm", output_file_name])
    for term in terms_dict.keys():
      writer.writerow((term, terms_dict[term]))

def extract(blast_csv_file_name, go_terms_csv_file_name):
  terms_dict = read_terms(blast_csv_file_name)
  write_terms(terms_dict, go_terms_csv_file_name)

if __name__ == '__main__':
  try:
    blast_csv_file_name = os.getenv('CONT_INPUT_BLAST_RESULTS_FILE')
    if blast_csv_file_name is None:
      raise Exception('Error: The CONT_INPUT_BLAST_RESULTS_FILE variable must be set')

    go_terms_csv_file_name = os.getenv('CONT_OUTPUT_GOTERMS_FILE')
    if go_terms_csv_file_name is None:
      raise Exception('Error: The CONT_OUTPUT_GOTERMS_FILE variable must be set')
    extract(blast_csv_file_name, go_terms_csv_file_name)
  except Exception as e:
    print e.message
    exit(1)

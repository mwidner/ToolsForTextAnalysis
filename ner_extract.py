'''
Take NER output from GATE
Extract entities

Usage: ner_extract.py (-i FILE ...) (-e ENTITY ...) [-o DIR]

-h --help   show this
-o --output DIR     specify output directory [default: ./results]
-i --input FILE 	specify input files
-e --entities		entities to extract

Mike Widner <mikewidner@stanford.edu>
'''

import os
import sys
from collections import defaultdict
from bs4 import BeautifulSoup
from docopt import docopt

options = docopt(__doc__)
entities = [e.lower() for e in options['--entities']]
entity_table = defaultdict(list)
OUTPUT_DIR = options['--output']

for filename in options['--input']:
	fh = open(filename, 'r')
	text = fh.read()
	fh.close()
	soup = BeautifulSoup(text)
	for item in soup.find_all(entities):
		entity_table[item.name].append(item.string)
	for entity_type in entity_table.keys():
		if not os.path.isdir(OUTPUT_DIR):
			os.makedirs(OUTPUT_DIR)
		key = os.path.basename(filename)
		key = os.path.splitext(key)[0]
		fh = open(OUTPUT_DIR + '/' + key + "_" + entity_type + ".txt", 'w')
		fh.write('\n'.join(entity_table[entity_type]))
		fh.close()
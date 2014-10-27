'''
Turns ngrams into network graphs
Uses output from bi_trigrams.py script, nltk-based collocations

Usage: ngrams2graph.py (-i FILE ...) [-l STRING ...] [-o FILE]

-h --help   show this
-o --output=FILE 	specify output file [default: ./ngram_network.gexf]
-l --label=STRING	specify a label for the central node; must be in the same order as file inputs
-i --input=FILE 	specify input CSV files

Mike Widner <mikewidner@stanford.edu>
'''

import os
import sys
import csv
import networkx as nx
from docopt import docopt

options = docopt(__doc__)
SOURCE = options['--input']
TARGET = options['--output']
LABELS = dict()
for filename in SOURCE:
	if options['--label']:
		LABELS[filename] = options['--label'].pop(0)
	else:
		LABELS[filename] = filename

def write_graph_file(ngrams):
	''' 
	Generate the network graph and write it 
	'''
	G = nx.DiGraph()
	for filename in ngrams.keys():
		G.add_node(LABELS[filename], label=LABELS[filename])
		G.add_nodes_from([ngram for ngram in ngrams[filename].values()])
		for item in ngrams[filename].items():
			G.add_edge(LABELS[filename], item[1], weight=item[0])
		try:
			nx.write_gexf(G, TARGET)
		except Exception as err:
			print("Could not write graphfile", TARGET, err)


def parse_ngram_csv(filename):
	'''
	Read in a CSV of ngrams with their measures as the first column
	Return a dict with the information
	'''
	results = dict()
	fh = open(filename, 'r')
	reader = csv.reader(fh)
	next(reader, None)	# skip header
	for row in reader:
		results[row[0]] = ' '.join(row[1:])
	fh.close()
	return(results)

def main():
	ngrams = dict()
	for filename in SOURCE:
		ngrams[filename] = parse_ngram_csv(filename)
		write_graph_file(ngrams)

if __name__ == '__main__':
  if sys.version_info[0] != 3:
    print("This script requires Python 3")
    exit(-1)
  main()

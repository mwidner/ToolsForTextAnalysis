"""
Read output from a corpus of text files
Create bigrams, trigrams, and frequency distributions

See documentation here: http://www.nltk.org/howto/collocations.html

Usage: bi_trigrams.py (-i DIR) (-o DIR) [-s FILE]

-h --help   show this
-o --output DIR      specify output directory [default: ./results]
-i --input DIR 		specify input directory	[default: .]
-s --stopwords FILE 	specify file containing list of stop words [default: ./stopwords.txt]

Mike Widner <mikewidner@stanford.edu>
"""

# how many n-grams to find
TOT_NGRAMS = 500
# how frequent must an n-gram be for inclusion
FREQ_FILTER = 3
# minimum character length of words to include
MIN_LENGTH = 4

import os
import csv
import nltk
import string
import itertools
import collections

from docopt import docopt

from nltk.corpus import PlaintextCorpusReader
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder, TrigramAssocMeasures, TrigramCollocationFinder

string.punctuation += "…"

options = docopt(__doc__)

SOURCE = options['--input'] + '/'	# added / to be safe
TARGET = options['--output'] + '/'

if not os.path.isdir(TARGET):
	os.makedirs(TARGET)

wordlists = PlaintextCorpusReader(SOURCE, ".*\.txt$")

bigram_measures = BigramAssocMeasures()
trigram_measures = TrigramAssocMeasures()

if options['--stopwords']:
	fh = open(options['--stopwords'], 'r')
	stopwords = fh.read()
	fh.close()
	stopwords = stopwords.split()
else:
	stopwords = False

def write_results(results, prefix):
	if not os.path.isdir(TARGET):
		os.makedirs(TARGET)

	# Bigrams
	fh = open(prefix + '-bigrams.txt', 'w')
	for bigram in results['bigrams']:
		fh.write(' '.join(bigram) + "\n")
	fh.close()
	fh = csv.writer(open(prefix + '-bigram_prefix.csv', 'w', encoding='utf-8'), dialect='excel')
	fh.writerow(['measure', 'first', 'second'])
	for key in results['b_prefix']:
		for item in results['b_prefix'][key]:
			fh.writerow([item[1], key, item[0]])	# funky ordering; fix it

	# Trigrams
	fh = open(prefix + '-trigrams.txt', 'w')
	for trigram in results['trigrams']:
		fh.write(' '.join(trigram) + "\n")
	fh.close()
	fh = csv.writer(open(prefix + '-trigram_prefix.csv', 'w', encoding='utf-8'))
	fh.writerow(['measure', 'first', 'second', 'third'])
	for key in results['t_prefix']:
		for item in results['t_prefix'][key]:
			fh.writerow([item[2], key, item[0], item[1]])

	# Freq Dist
	fh = csv.writer(open(prefix + '-fdist.csv', 'w', encoding='utf-8'), dialect='excel')
	fh.writerow(['word', 'raw_frequency'])
	for word in results['fdist'].keys():
		fh.writerow([word, results['fdist'][word]])

def analyze_text(text, filename):
	print(len(text), filename)
	words = [w.lower() for w in text 
				if w not in string.punctuation 
				if w.lower() not in stopwords
				and len(w) >= MIN_LENGTH]

	fdist = nltk.FreqDist(words)

	# what follows could totally be generalized
	# Bigrams
	print("Generating bigrams from", filename)
	b_finder = BigramCollocationFinder.from_words(words)
	b_finder.apply_freq_filter(FREQ_FILTER)
	# if stopwords:
	# 	b_finder.apply_word_filter(lambda w: w in stopwords)
	bigrams = b_finder.nbest(bigram_measures.pmi, TOT_NGRAMS)
	b_scored = b_finder.score_ngrams(bigram_measures.pmi)
	b_prefix_keys = collections.defaultdict(list)
	for key, scores in b_scored:
		b_prefix_keys[key[0]].append((key[1], scores))

	# Trigrams
	print("Generating trigrams from", filename)
	t_finder = TrigramCollocationFinder.from_words(words)
	t_finder.apply_freq_filter(FREQ_FILTER)
	# if stopwords:
	# 	t_finder.apply_word_filter(lambda w: w in stopwords)
	trigrams = t_finder.nbest(trigram_measures.pmi, TOT_NGRAMS)
	t_scored = t_finder.score_ngrams(trigram_measures.pmi)
	t_prefix_keys = collections.defaultdict(list)
	for key, scores in t_scored:
		t_prefix_keys[key[0]].append((key[1], key[2], scores))

	return({'bigrams': bigrams, 'b_prefix': b_prefix_keys, 
			'trigrams': trigrams, 't_prefix': t_prefix_keys, 
			'fdist': fdist})

wc_fh = csv.writer(open(TARGET + 'word_counts.csv', 'w', encoding='utf-8'))
wc_fh.writerow(['year', 'words'])
# Per file results
for filename in wordlists.fileids():
	if len(wordlists.raw(fileids=[filename])) == 0:
		continue
	slug = filename.partition(".")[0]	# grab a filename
	wc_fh.writerow([slug, len(wordlists.words(fileids=[filename]))])
	results = analyze_text(wordlists.words(fileids=[filename]), filename)
	write_results(results, TARGET + slug)

# Cumulative results
# Note: chokes on empty files
wc_fh.writerow(['all', len(wordlists.words())])
results = analyze_text(wordlists.words(), "all")
write_results(results, TARGET + "all")
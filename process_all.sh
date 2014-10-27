#!/bin/sh
#
# Run the text analysis scripts
#
#####

python slice_corpus.py
python bi_trigrams.py -i corpora/author -o results/author/ngrams/ -s stopwords.txt
python ngrams2graph.py -i results/author/ngrams/author1-bigram_prefix.csv -l "Author 1 Name" -i results/author/ngrams/author2-bigram_prefix.csv -l "Author 2 Name" -o results/author/ngrams/bigrams.gexf

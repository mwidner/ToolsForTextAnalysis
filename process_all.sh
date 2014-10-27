#!/bin/sh
#
# Run the text analysis scripts
#
#####

python slice_corpus.py
python bi_trigrams.py -i corpora/author -o results/author/ngrams/ -s stopwords.txt
python ngrams2graph.py -i results/author/ngrams/JMLP-bigram_prefix.csv -l "Jean-Marie Le Pen" -i results/author/ngrams/MLP-bigram_prefix.csv -l "Marine Le Pen" -o results/author/ngrams/bigrams.gexf
python ngrams2graph.py -i results/author/ngrams/JMLP-trigram_prefix.csv -l "Jean-Marie Le Pen" -i results/author/ngrams/MLP-trigram_prefix.csv -l "Marine Le Pen" -o results/author/ngrams/trigrams.gexf

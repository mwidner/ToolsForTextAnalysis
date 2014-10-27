#!/bin/sh

FILES=`ls results/ngrams/author/genre/stripped/*-trigram_prefix.csv`
CMD="python scripts/ngrams2graph.py"
for FILE in $FILES
	do
		CMD="$CMD -i $FILE "
	done
CMD="$CMD -o results/ngrams/author/genre/stripped/all_trigram_network.gexf"
eval $CMD
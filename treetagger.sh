#!/bin/bash
FILES=/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/corpora/author/genre/*
for file in $FILES
do
	echo $file
	FILENAME=`echo $file | /usr/bin/awk 'BEGIN{FS="/"}{print $NF}'`
	/Applications/TreeTagger/cmd/tagger-chunker-french $file > /Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/results/treetagger/author/genre/$FILENAME
done
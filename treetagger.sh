#!/bin/bash
FILES=PATH/*
for file in $FILES
do
	echo $file
	FILENAME=`echo $file | /usr/bin/awk 'BEGIN{FS="/"}{print $NF}'`
	/Applications/TreeTagger/cmd/tagger-chunker-french $file > /OUTPUT/$FILENAME
done

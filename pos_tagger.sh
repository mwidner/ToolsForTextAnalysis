#!/bin/sh

DOC_PATH="./"
FILES=`ls ${DOC_PATH}/*.txt`
TT_FR="/Applications/TreeTagger/cmd/tagger-chunker-french"
RESULTS_DIR="./results"

if [ ! -d $RESULTS_DIR ];
	then
		mkdir -p $RESULTS_DIR
fi

for FILE in ${FILES}
	do
		FILENAME=`echo $FILE | /usr/bin/awk 'BEGIN{FS="/"}{print $NF}'`
		/bin/cat ${FILE} | $TT_FR > ${RESULTS_DIR}/tagged_${FILENAME}
	done

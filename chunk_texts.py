'''
Chunks a list of files into parts for topic modeling
Reads in a CSV file of the filenames to chunk
Uses rough word counts; nothing in this world is perfect

Mike Widner <mikewidner@stanford.edu>
'''
import sys
import csv
import os

MIN_LENGTH=250	# minimum words in a chunk
CHUNK_SIZE=500	# number of words per chunk

csv.field_size_limit(sys.maxsize) # Otherwise CSV chokes on the big text fields

def chunker(words):
	chunk_list = []
	chunk = []
	i = 0
	while words:
		word = words.pop()
		chunk.append(word)
		i += 1
		if i >= CHUNK_SIZE:
			chunk_list.append(chunk)
			chunk = []
			i = 0
	if (len(chunk) < MIN_LENGTH and len(chunk_list) > 0):
		chunk_list[len(chunk_list) - 1].extend(chunk)
	elif (chunk):
		chunk_list.append(chunk)
	return(chunk_list)

out_dir = os.path.dirname(os.path.realpath(__file__)) + '/chunks'
if not os.path.exists(out_dir):
	os.mkdir(out_dir)

reader = csv.DictReader(open(sys.argv[1], "r"), quoting=csv.QUOTE_ALL)
for row in reader:
	doc_dir = out_dir + "/" + row['filename']
	if not os.path.exists(doc_dir):
		os.makedirs(doc_dir)
	try:
		fh = open(row['filename'], 'r')
		text = fh.read()
		fh.close()
	except FileNotFoundError as err:
		print("File not found:", err)
		continue

	chunks = chunker(text.split())
	i = 0
	for chunk in chunks:
		fh = open(doc_dir + '/' + str(i), "w")
		fh.write(' '.join(chunk))
		fh.write("\n")
		i += 1
		fh.close()
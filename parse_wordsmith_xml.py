'''
For Cécile Alduy's Rhetoric of LePen project
Parses WordSmith XML output of keyness

Mike Widner <mikewidner@stanford.edu>
'''
import csv
import collections
import sys
import string
import numpy as np
import pandas as pd
import xmltodict

# list of files holding metadata about our texts
metadata = ['JMLP_discours.csv',
			'MLP_discours.csv',
			'JMLP_radio.csv',
			'MLP_radio.csv',
			'JMLP_tv.csv',
			'MLP_tv.csv']
basedir = '/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/'
corpora = basedir + 'corpora/'

# Add punctuation that appears in corpus to what we strip
string.punctuation += '…'

def count_words(filename):
	''' Count all the words in a file; return dictionary '''
	counts = collections.defaultdict(int)
	total = 0
	fh = open(filename, 'r', encoding='utf-8')
	for line in fh:
		words = line.split()
		for word in words:
			word = word.strip(string.punctuation).lower()
			counts[word] += 1
			total += 1
	return({'counts': counts, 'total': total})

def main(): 
	''' Convert wordsmith output '''
	# keyword, freq, percent, keyness, texts
	fh = open(corpora + 'JMLP/' + 'keywords_all.xml', "r", encoding='utf-8')
	data = fh.read()
	fh.close()
	fh = open(basedir + 'stopwords.txt', 'r')
	stopwords = [w.rstrip() for w in fh]
	fh.close()
	keyword_data = xmltodict.parse(data)
	keyword_data = keyword_data['WordSmith_XML_Data']['XML_Row']
	keyword_df = pd.DataFrame([row for row in keyword_data])
	# re-cast data types
	data_types = {'int':['freq','texts','rc_freq'], 
				'float':['keyness','percent','rc_percent']}
	# for k,v in data_types:	#TODO: work w/ new data_types structure
	# 	try:
	# 		keyword_df[k] = keyword_df[k].astype(data_types[k])
	# 	except ValueError as err:
	# 		print(err, k)
	# drop columns we don't want
	keyword_df.drop('Lemmas', inplace=True, axis=1)
	keyword_df.drop('N', inplace=True, axis=1)
	keyword_df.drop('P', inplace=True, axis=1)
	keyword_df.drop('Set', inplace=True, axis=1)
	keyword_df.keyword = keyword_df.keyword.str.lower()
	keyword_df = keyword_df[~keyword_df.keyword.isin(stopwords)] # strip stop words
	keyword_df.sort_index(by=['freq'], ascending=False).to_csv('keywords.csv')


	# keyword_df.to_csv('keywords.csv', encoding='utf-8')
	# fh = open(basedir + 'words_of_interest', 'r')
	# targets = [w.rstrip() for w in fh]
	# fh.close()

	# targets_df = pd.DataFrame(targets, columns=['keyword'])

	# # actually not useful; words of interest mostly not found
	# word_list_df = pd.merge(targets_df, keyword_df)
	# print(keyword_df)
	# word_list_df.to_csv('interest_freq.csv')
	# print(keyword_df['keyword'].isin(stopwords_df))

	exit()
	texts = []	# build up data for a DataFrame
	for filename in metadata:
		with open(basedir + filename, 'r', encoding='utf-8') as fh:
			try:
				reader = csv.DictReader(fh)
				# Columns: rid,filename,author,title,date,type,publication,place,length,collection,preparer
				for row in reader:
					# print("Processing " + row['filename'])
					ret = count_words(corpora + row['filename'])
					# row['data'] = pd.DataFrame([ret['counts']])
					row['data'] = pd.Series(ret['counts'])
					row['total'] = ret['total']
					texts.append(row)
			except FileNotFoundError as err:
				print("Missing file: " + basedir + row['filename'])
	df_texts = pd.DataFrame(texts)
	fh = open(basedir + 'words_of_interest', 'r')
	targets = []
	# df_words = pd.DataFrame(df_texts['data'])

	for t in fh:
		targets.append(t.rstrip())
	fh.close()
	# s_targets = pd.Series(targets)

	# most common words
	# df_texts.ix[i]['data'].order(ascending = False).head()

	# Probably not the best way to do this
	results = list()
	for i, s in df_texts['data'].iteritems():
		row = df_texts.ix[i]
		results.append(dict())
		results[i]['filename'] = row['filename']
		results[i]['total words'] = row['total']
		results[i]['author'] = row['author']
		results[i]['type'] = row['type']
		results[i]['filename'] = row['filename']
		results[i]['date'] = pd.to_datetime(row['date'], dayfirst=True, coerce=True)
		# print(date, author, genre, filename, tot)
		for word in targets:
			try:
				c = s.loc[word.lower()]
			except: 
				c = 0
			finally:
				results[i][word] = c 

				# print(word, c, c / tot)

	# create many groupings
	df_results = pd.DataFrame(results)
	groups = ['date', 'author', 'type']
	df_date = df_results.groupby('date')
	df_author = df_date.groupby('author')

if __name__ == '__main__':
	if sys.version_info[0] != 3:
	    print("This script requires Python 3")
	    exit(-1)
	main()
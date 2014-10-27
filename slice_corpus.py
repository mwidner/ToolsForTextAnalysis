'''
The Corpus Slicer

Read in an Excel file with multiple sheets of metadata describing corpus and file locations
Organize and slice the text files for analysis and further processing

Mike Widner <mikewidner@stanford.edu>
'''
import os
import csv
import sys
# import nltk
import pandas as pd
import datetime as dt

BASEDIR = '/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/'
WORKBOOK = BASEDIR + 'metadata/LePen Corpus Metadata.xlsx'
SOURCE = BASEDIR + 'corpora_raw/Database CLEAN Book LePen2014/'
TARGET = BASEDIR + 'corpora/'

# sheets to ignore; names should be all lower-cased here
ignore_sheets = ['all transcribed dropbox files', 'transcribed but not cleaned']

# to rename some columns for easier/more legible access later
column_maps = {'date (dd/mm/yyyy)': 'date', 'type of media': 'genre'}

# rename our genres to something more legible
genre_maps = {'DL Radio': 'radio', 
				'DL Radio ': 'radio', 
				'CabSat': 'television', 
				'DLTV': 'television',
				'éditorial ': 'éditorial'
				}

def get_year(value):
	'''
	Return a 4 digit year based on the given value
	'''
	if isinstance(value, dt.datetime):
		return(int(value.year))
	(day, month, year) = value.split('/')
	year = year[-2:].strip()
	if len(year) == 1:
		year = "0" + year 	# hacky fix for messed up data
	if int(year) <= 99 and int(year) >= 80:
		year = "19" + year
	else:
		year = "20" + year
	return(int(year))

def load_words(filename):
	'''
	Open and read a text file
	Return contents as raw string
	''' 
	words = list()
	raw = str()
	try:
		fh = open(SOURCE + filename, "r")
		raw = fh.read()
		fh.close()
		# wordlist = nltk.corpus.PlaintextCorpusReader(SOURCE, filename)
		# words = wordlist.words(fileids=[filename])
	except OSError as err:
		print("Missing: " + filename)
	return(raw)

def generate_text(df, dirname, filename):
	'''
	Takes all words for a given slice
	Write out as a single text file
	'''
	if (len(df['words']) == 0):
		return 	# don't write empty files
	print("Generating " + dirname + filename + '.txt')
	path = TARGET + dirname
	if not os.path.isdir(path):
		os.makedirs(path)
	fh = open(path + filename + '.txt', 'w')
	for row in df['words']:
		fh.write(row)
	fh.close()

def get_unique(df, key):
	'''
	Return an array of unique values for the given column name/key
	'''
	return(pd.unique(df[key].values.ravel()))

def main(): 
	''' 
	Process metadata spreadsheet
	Organize by different slicings
	'''
	df = pd.DataFrame()
	workbook = pd.ExcelFile(WORKBOOK)
	sheet_list = list()
	for sheet in [s for s in workbook.sheet_names if s.lower() not in ignore_sheets]:
		sheet_list.append(workbook.parse(sheet))
	df = pd.concat(sheet_list)
	df.rename(columns=column_maps, inplace=True) # fix our column names
	df['genre'].replace(genre_maps, inplace=True)	# fix genre values
	df['year'] = df['date'].apply(get_year)
	df['basename'] = df['filename'].apply(os.path.basename)
	df['words'] = df['filename'].apply(load_words)	# load words for every file

	# get lists of our unique values for each column
	years = get_unique(df, 'year')
	authors = get_unique(df, 'author')
	genres = get_unique(df, 'genre')

	# now iterate through our desired slices and generate new text files
	for year in years:
		generate_text(df[df['year'] == year], 'year/', str(year))
	for genre in genres:
		generate_text(df[df['genre'] == genre], 'genre/', str(genre))
	for author in authors:
		generate_text(df[df['author'] == author], 'author/', str(author))
		# by author and by genre
		df_author = df[df['author'] == author]
		pd.options.mode.chained_assignment = None	# disable warnings on next line
		df_author.drop('date', inplace = True, axis = 1)	 # some conversion bug on dates
		for genre in genres:
			df_genre = df[df['genre'] == genre]
			df_genre.drop('date', inplace = True, axis = 1)
			df_join = pd.merge(df_author, df_genre)
			generate_text(df_join, 'author/genre/', str(author) + '_' + str(genre))

if __name__ == '__main__':
	if sys.version_info[0] != 3:
	    print("This script requires Python 3")
	    exit(-1)
	main()
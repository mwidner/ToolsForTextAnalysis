'''
Get Front National corpus from Marine Le Pen's works on their website

Mike Widner <mikewidner@stanford.edu>
'''

from bs4 import BeautifulSoup
import requests
# import lxml.html

START_URL = 'http://www.frontnational.com/author/marinelepen/'
END_URL = 'http://www.frontnational.com/author/marinelepen/page/21/'

OUTPUT_DIR = '/Users/widner/Projects/DLCL/Alduy/Rhetoric_of_LePen/scrapy'

r = requests.get(START_URL)

soup = BeautifulSoup(r.text)
# from paged view:
# title: .pk_entry_title > a.title
# metadata div: .pk_entry_meta > .pk_full
# content div: .pk_entry_content > p (<strong> is desc?); after <br/>

# from article:
# div.pk_entry_full > div.pk_two_third-blog > p (multiple elements)
# maybe pk_last is more reliable?
for post in soup.find_all('div', 'post'):
	print(post)
	break

def parse_page(content):
	'''
	Parse the content of a full article
	'''
	pass

def parse_view(content):
	'''
	Parse the data on a page view of posts
	'''
	pass

def iterate_over_pages(url):
	'''
	Request each paged view of MLP's posts
	'''
	pass



#!/usr/bin/env python

from collections import defaultdict
import httplib2
import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import os
import pandas as pd



def httpget(website, tempname):
	"""download website and save to temp/tempname"""
	#http = httplib2.Http()
	#status, response = http.request('http://'+website+'/')
	req = urllib2.Request('http://'+website)
	response = urllib2.urlopen(req)
	the_page = response.read()
	with open('temp/'+tempname, 'w') as filename:
		filename.write(the_page)
	return

def httpparse(tempname):
	"""parse http or https links in the downloaded webpage"""
	the_page = open('temp/'+tempname, 'r').read()
	soup = BeautifulSoup(the_page)
	soup.prettify()
	all_links = []

	#TODO: add images or other links apart from href?
	#TODO: this saves all links local and http/https - need to parse
	for anchor in soup.findAll('a', href=True):
		#print anchor['href']
		all_links.append(anchor['href'])
	#for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
	#	if link.has_attr('href'):
	#		print link['href']
	#return link['href']
	return all_links


data = defaultdict(list)
# read top 100 alexa
ctr = 0
for website in open('top-100.txt', 'r').readlines():
	print ctr, website
	tempname = 'page'+str(ctr)
	ctr+=1

# download top 100 home pages
	httpget(website, tempname)

# parse home pages for http links
	list_of_links = httpparse(tempname)

	data['rank'].append(ctr)
	data['website'].append(website)
	data['page'].append(tempname)
	data['links'].append(list_of_links)	

	df = pd.DataFrame.from_dict(data)
	df.to_pickle('top-100.pkl')

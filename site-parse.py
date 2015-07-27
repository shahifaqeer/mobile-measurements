#!/usr/bin/env python

from collections import defaultdict
import os


def httpget(website, tempname):
	"""download website and save to temp/tempname"""
	pass

def httpparse(tempname):
	"""parse http or https links in the downloaded webpage"""
	pass


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
	

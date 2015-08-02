#!/usr/bin/env python

from collections import defaultdict
#import httplib2
import urllib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
import os, sys, json
import pandas as pd
from topsites.topsites import topSites


OUTPUTFILE = 'data/top-%s.json'

def httpGet(website, tempname):
    """download website and save to temp/tempname"""
    #http = httplib2.Http()
    #status, response = http.request('http://'+website+'/')
    website = website.lower()
    try:
        req = urllib2.Request('http://'+website+'/')
        response = urllib2.urlopen(req)
        the_page = response.read()
    except:
        try:
            req = urllib2.Request('http://www.'+website+'/')
            response = urllib2.urlopen(req)
            the_page = response.read()
        except:
            print "COUDN'T LOAD http://www."+website
            the_page = ''

    with open('temp/'+tempname, 'w') as filename:
        filename.write(the_page)
    return

def httpParse(tempname):
    """parse http or https links in the downloaded webpage"""
    the_page = open('temp/'+tempname, 'r').read()
    soup = BeautifulSoup(the_page)
    soup.prettify()
    all_links = []
    temp_links = []

    #TODO: add images or other links apart from href?
    #TODO: this saves all links local and http/https - need to parse
    for anchor in soup.findAll('a', href=True):
        #print anchor['href']
        # use unicode to make links non-navigable
        link = unicode(anchor['href'])
        all_links.append( link )

        # create link set from list_of_links
        split_link = link.split("/")
        # if external link
        if 'http' in split_link[0]:
            temp_links.append(split_link[2])
    #for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
    #	if link.has_attr('href'):
    #		print link['href']
    #return link['href']

    # take set of external links
    link_set = list(set(temp_links))

    return all_links, link_set

def readTop(country, count):
    # read top 100 alexa

    Global = False
    if country.lower() == 'global':
        Global = True
        country_code = 'global'
    else:
        country_code = country.upper()

    data = defaultdict(list)

    # download or read top alexa list offline if count is 0
    if count == 0 or count=='0':
        filename = 'top-%s.json' %(country_code)
        with open(filename, 'r') as fr:
            site_list = json.load(fr)
    else:
        site_list = topSites( (country, count) )
    print country, count, site_list

    for rank, website in site_list:
	print rank, website
	tempname = 'page'+rank+'.html'

        # download top 100 home pages
        httpGet(website, tempname)

        # parse home pages for http links
	list_of_links, link_set = httpParse(tempname)

	data['rank'].append(rank)
	data['website'].append(website)
	data['page'].append(tempname)
	data['links'].append(list_of_links)
	data['link_set'].append(link_set)

    #df = pd.DataFrame.from_dict(data)
    #print df
    #df.to_pickle( OUTPUTFILE %(country_code) )
    with open( OUTPUTFILE %(country_code), 'w') as fp:
        json.dump(data, fp)

    return


if __name__=='__main__':

    if len(sys.argv) != 3:
        sys.stderr.write('Usage: COUNTRY-CODE TOP-N\nTo use offline list use COUNT=0\n')
        sys.exit(1)
    argv = (sys.argv[1], sys.argv[2])

    # currently only multiples of 25 are accepted as count
    print "TEST ", argv
    readTop(argv[0], argv[1])


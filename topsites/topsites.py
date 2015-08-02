#!/usr/bin/env python
from bs4 import BeautifulSoup
import requests
import sys
from math import ceil
import json

BASE_URL='http://www.alexa.com/topsites/countries;%d/%s'
BASE_URL_Global = 'http://www.alexa.com/topsites/global;%d'
Default_URL_Global = 'http://www.alexa.com/topsites/'
OUTPUTFILE = 'top-%s.json'

def topSites(argv):
    # (Country Code, # of top websites)
    site_list = []
    Global = False
    if argv[0].lower() == 'global':
        Global = True
    else:
        country_code = argv[0].upper()
    number = int(argv[1])
    delimiter = ' '

    page_numbers = int(ceil(number/25.0))
    for page_num in range(0, page_numbers):
        if Global == True:
            if page_num > 0:
                response = requests.get(BASE_URL_Global % (page_num))
            else:
                response = requests.get(Default_URL_Global)
                #print response
        else:
            response = requests.get(BASE_URL % (page_num, country_code))

        soup = BeautifulSoup(response.text)
        bullets = soup.find_all('li', {'class':'site-listing'})

        for bullet in bullets:
            rank = bullet.div.contents[0]
            site = bullet.p.a.contents[0]
            site_list.append((rank, site))
            #print('%s%s%s' % (rank, delimiter, site))

    if Global == True:
        global_top = []
        for site in site_list:
            global_top.append(site[1])
        with open( (OUTPUTFILE %('global')), 'w') as outfile:
            json.dump(global_top, outfile)

    else:
        country_top = []
        for site in site_list:
            country_top.append(site[1])
        with open( (OUTPUTFILE %(country_code)), 'w') as outfile:
            json.dump(country_top, outfile)

    return site_list

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write('Usage: COUNTRY-CODE TOP-N\n')
        sys.exit(1)
    argv = (sys.argv[1], sys.argv[2])
    site_list = topSites(argv)



#############################################
# author: Arpit Gupta (glex.qsd@gmail.com)  #
#############################################

from topsites import topSites
import json

K = 25 # Number of uniques we want
N= 150 # Sample space

blackList = {'Icmwebserv.com', 'Sudani.sd', 'Supremecluster.com', 'Nedsecure.co.za', 'Orange.mg'}

def getTopfromAtlasHostCountries():
    cc = {}
    top_sites = {}
    with open("../country_code_AF.txt") as f:        
        for line in f.readlines():
            tmp = line.split('\t')
            cc[tmp[1]] = tmp[0]
    with open("../activeAfricanProbes.json") as f:
        cntry2probes = json.load(f)
           
    for country in cc.keys(): 
        if country in cntry2probes.keys():
            tmp = topSites((country, N))
            if len(tmp) > 0:       
                top_sites[country] = topSites((country, N))
                print cc[country], len(tmp)
    top_sites['global'] = topSites(('global', K))
    print "Countries: ", len(top_sites.keys())
    with open('../countryTop.json', 'w') as outfile:
      json.dump(top_sites, outfile)
    return 


def getTop25Unique(top_sites):
    top_unique = {}
    globalTop = [elem[1] for elem in top_sites['global']]
    countries = [elem for elem in top_sites.keys() if elem!='global']
    for country in countries:
        unique = []
        print globalTop
        for site in top_sites[country]:
            site = site[1]
            if site not in globalTop:
                if site not in blackList:
                    print country, site
                    unique.append(site)
                    if len(unique) == K:
                        break
            else:
                print "Not Unique", site
        top_unique[country] = unique
    with open('../topUnique.json', 'w') as outfile:
      json.dump(top_unique, outfile)
        

if __name__ == '__main__':
    #top_sites = getTopfromAtlasHostCountries()
    with open("../countryTop.json") as f:
        top_sites = json.load(f)
    getTop25Unique(top_sites)
    
        
        
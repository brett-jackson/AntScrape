#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 15:33:15 2019

@author: brettjackson
"""

import requests
import json
class AntMound:
    def __init__(self):
        self.url = 'https://antmaps.org/api/v01/'
        self.bentities = json.loads(requests.get(self.url+'bentities.json',verify=False).text)['bentities']
#        with open('bentities.json') as f:
#            self.countries = json.load(f)['bentities']
    def byLocation(self,location,write=True):
        bentity= ''
        for row in self.bentities:
            if location.casefold() == row['display'].casefold():
                bentity = row['key']
        genus=''
        subfamily=''
        query = self.url + 'species.json?bentity_id=' + bentity + '&genus=' + genus + '&subfamily=' + subfamily
        species = json.loads(requests.get(query,verify=False).text)['species']
        if write:
            print(species)
            with open(location.casefold()+'.txt','w') as f:
                antList = [ant['display'] for ant in species]
                for ant in antList:
                    f.write(ant+'\n')
        return species
    
    def bySpecies(self,species,write=True):
        species = species.strip()
        species = species.replace(' ','.')
        query = self.url+'species-range.json?species=' + species
        locations = json.loads(requests.get(query,verify=False).text)['bentities']
        for loc in locations:
            loc['location']=[bent['display'] for bent in self.bentities][[bent['key'] for bent in self.bentities].index(loc['gid'])]
        if write:
            print(locations)
            with open(species.replace('.','_')+'.txt','w') as f:
                locList = [loc for loc in locations]
                for loc in locList:
                    f.write(loc['location']+'\n')
        return locations
    
if __name__ == '__main__':
    ants = AntMound()
    antList   = ants.byLocation('Missouri')
    placeList = ants.bySpecies(antList[0]['key'])
    

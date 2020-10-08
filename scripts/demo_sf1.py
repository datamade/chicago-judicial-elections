import json
import sys

import scrapelib
import tqdm
from scrapelib.cache import FileCache
from census_area import Census

s = scrapelib.Scraper(raise_errors=False, requests_per_minute=0)
cache = FileCache('cache')

s.cache_storage = cache
s.cache_write_only = False

API_KEY = 'ac94ba69718a7e1da4f89c6d218b8f6b5ae9ac49'

geographies = json.load(sys.stdin)
c = Census(API_KEY, session=s, year=int(sys.argv[1]))

VARS = {'P008001': 0, # total population,
        'P008003': 0, # Not Hispanic or Latino white
        'P008004': 0, # Not Hispanic or Latino black
        'P008006': 0, # Not Hispanic or Latino asian
        'P008010': 0, # Hispanic or Latino
        }

READABLE_VARS = {'geography number': None,
                 'P008001': 'Total Population',
                 'P008003': 'Not Hispanic or Latino Origin, Whites',
                 'P008004': 'Not Hispanic or Latino Origin, Blacks',
                 'P008006': 'Not Hispanic or Latino Origin, Asians',
                 'P008010': 'Hispanic or Latino Origin',
                 'number of tracts': None}

for geography in tqdm.tqdm(geographies['features']):
    geography_data = VARS.copy()
    geography_geo = geography['geometry']

    tracts = c.sf1.geo_tract(('NAME',) + tuple(VARS), geography_geo)
    total_tracts = 0
    for geojson, data, weight in tracts:                
        for var in VARS:
            assert var in data, (data, weight, geojson)
            geography_data[var] += (data[var] * weight)
        total_tracts += weight 

    geography_data = {k: int(v) for k, v in geography_data.items() if v is not None}
    geography_data['number of tracts'] = total_tracts

    geography['properties'].update(geography_data)

json.dump(geographies, sys.stdout)

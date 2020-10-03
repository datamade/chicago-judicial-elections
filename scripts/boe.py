import json
import sys
import argparse
import logging

from chi_elections.precincts import elections
import scrapelib
from scrapelib.cache import FileCache


logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='Chicago municipal election results')
parser.add_argument('--year', type=int, help='year of election')
parser.add_argument('--type', type=str, choices=('general', 'primary'), help='type of election')
# parser.add_argument('geojson', type=argparse.FileType('r'), help='geojson of precincts')


args = parser.parse_args()

# precincts = json.load(args.geojson)

# precinct_features = {}
# for feature in precincts['features']:
#     properties = feature['properties']
#     for k in list(properties.keys()):
#         if k not in ("WARD", "PRECINCT"):
#             del properties[k]
#     precinct = (properties['WARD'], properties['PRECINCT'])
#     precinct_features[precinct] = properties

cache = FileCache('_cache')

session = scrapelib.Scraper()
session.cache_storage = cache
session.cache_write_only = False

elections = elections(session)
print(elections, file=sys.stderr)
elections = [(name, election) for name, election in
             elections.items()
             if (str(args.year) in name
                 and (args.type in name.lower()
                      or (args.type == 'general' and 'geeral' in name.lower())))]

if args.type == 'general':
    assert len(elections) == 1, elections
elif args.type == 'primary':
    assert 2 < len(elections) < 5, elections

election_results = {name: {} for name, _ in elections}
all_candidates = set()

scrape_remaining = False
for election_name, election in elections:
    for race_name, race in election.races.items():
        if 'judge' in race_name.lower() or scrape_remaining:
            if args.type == 'general':
                scrape_remaining = True
            try:
                results = race.precincts.items()
            except scrapelib.HTTPError:
                continue
            for precinct, votes in results:
                precinct = str(precinct)
                votes = {race_name: votes}
                if precinct in election_results[election_name]:
                    election_results[election_name][precinct].update(votes)
                else:
                    election_results[election_name][precinct] = votes
                all_candidates.update(votes.keys())
    for precinct, votes in election.turnout.precincts.items():
        precinct = str(precinct)
        if precinct in election_results[election_name]:
            election_results[election_name][precinct].update(votes)
        else:
            election_results[election_name][precinct] = votes
        all_candidates.update(votes.keys())

# for precinct, votes in election_results.items():
#     other_candidates = all_candidates - votes.keys()
#     precinct_features[precinct].update(votes)
#     precinct_features[precinct].update({cand: None for cand in other_candidates})
    

# if args.type == 'general':
#     for precinct in precinct_features:
#         assert election_results[precinct]
# else:
#     for precinct in precinct_features:
#         if precinct not in election_results:
#             precinct_features[precinct].update({cand: None for cand in all_candidates})
    
with sys.stdout as f:
    json.dump(election_results, f)


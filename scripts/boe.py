import sys
import argparse
import logging
import csv

from chi_elections.precincts import elections
import scrapelib
from scrapelib.cache import FileCache


logging.basicConfig(level=logging.DEBUG)

parser = argparse.ArgumentParser(description='Chicago municipal election results')
parser.add_argument('--year', type=int, help='year of election')
parser.add_argument('--type', type=str, choices=('general', 'primary'), help='type of election')
parser.add_argument('--party', type=str, choices=('dem', 'rep'), help='party primary')

args = parser.parse_args()

if (args.type == 'primary') and (args.party is None):
    parser.error('--party must be given if the election type is "primary"')

cache = FileCache('_cache')

session = scrapelib.Scraper()
session.cache_storage = cache  # type: ignore
session.cache_write_only = False

elections = elections(session)
election, = [election for name, election in
             elections.items()
             if (str(args.year) in name
                 and (args.type in name.lower()
                      or (args.type == 'general' and 'geeral' in name.lower()))
                 and (args.party is None or args.party in name.lower()))]

election_results = {}
all_candidates = set()

scrape_remaining = False
for race_name, race in election.races.items():
    if 'judge' in race_name.lower() or scrape_remaining:
        if args.type == 'general':
            scrape_remaining = True
        try:
            results = race.precincts.items()
        except scrapelib.HTTPError:
            continue
        for precinct, votes in results:
            votes = {race_name: votes}
            if precinct in election_results:
                election_results[precinct].update(votes)
            else:
                election_results[precinct] = votes
            all_candidates.update(votes.keys())


for precinct, votes in election.turnout.precincts.items():
    if precinct in election_results:
        election_results[precinct].update(votes)
    else:
        election_results[precinct] = votes
    all_candidates.update(votes.keys())

field_names = ['WARD', 'PRECINCT', 'REGISTERED VOTERS', 'BALLOTS CAST', 'RACE', 'CANDIDATE', 'VOTES']
writer = csv.DictWriter(sys.stdout, fieldnames=field_names, dialect='unix')
writer.writeheader()

for (ward, precinct), results in election_results.items():
    precinct_level = {k: results[k] for k in ('REGISTERED VOTERS', 'BALLOTS CAST')}
    precinct_level['WARD'] = ward
    precinct_level['PRECINCT'] = precinct
    for race in results.keys() - set(field_names):
        for candidate, votes in results[race].items():
            candidate_level = precinct_level.copy()
            candidate_level.update({'RACE': race.strip(),
                                    'CANDIDATE': candidate.strip(),
                                    'VOTES': votes})
            writer.writerow(candidate_level)

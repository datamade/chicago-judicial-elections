import sys
import csv
import json

precincts = json.load(sys.stdin)
features = precincts['features']

field_names = list(features[0]['properties'].keys())

field_names.remove('WARD')
field_names.remove('PRECINCT')
field_names.remove('REGISTERED VOTERS')
field_names.remove('BALLOTS CAST')

field_names = ['WARD', 'PRECINCT', 'REGISTERED VOTERS', 'BALLOTS CAST', 'RACE', 'CANDIDATE', 'VOTES']

writer = csv.DictWriter(sys.stdout, fieldnames=field_names, dialect='unix')
writer.writeheader()
for feature in features:
    properties = feature['properties']
    try:
        precinct_level = {k: properties[k] for k in field_names[:4]}
    except:
        print(properties, file=sys.stderr)
        raise
    for race in properties.keys() - set(field_names):
        for candidate, votes in properties[race].items():
            candidate_level = precinct_level.copy()
            candidate_level.update({'RACE': race.strip(),
                                    'CANDIDATE': candidate.strip(),
                                    'VOTES': votes})
            writer.writerow(candidate_level)

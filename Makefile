.DELETE_ON_ERROR :

.PHONY : all
all : data/judicial_primary_2020.geojson data/judicial_general_2018.geojson \
      data/judicial_primary_2018.geojson data/judicial_general_2016.geojson \
      data/judicial_primary_2016.geojson data/judicial_general_2014.geojson \
      data/judicial_primary_2014.geojson data/judicial_general_2012.geojson \
      data/judicial_primary_2012.geojson data/judicial_general_2010.geojson \
      data/judicial_primary_2010.geojson data/judicial_general_2008.geojson \
      data/judicial_primary_2008.geojson data/judicial_general_2006.geojson \
      data/judicial_primary_2006.geojson data/judicial_general_2004.geojson \
	  data/judicial_primary_2004.geojson data/judicial_general_2002.geojson \
      data/judicial_primary_2002.geojson data/judicial_general_2000.geojson \
      data/judicial_primary_2000.geojson

data/judicial_primary_%.geojson : 
	python scripts/boe.py $< --year=$* --type=primary > $@

data/judicial_general_%.geojson : 
	python scripts/boe.py $< --year=$* --type=general > $@

%.csv : %.geojson
	cat $< | python scripts/json_to_csv.py | csvsort > $@

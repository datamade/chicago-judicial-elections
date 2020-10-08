.DELETE_ON_ERROR :

GENERAL_YEARS = 2018 2016 2014 2012 2010 2008 2006 2004 2002 2000
PRIMARY_YEARS = 2020 $(GENERAL_YEARS)

DEMOCRATIC_PRIMARIES = $(patsubst %,data/wards/judicial_democratic_primary_%.csv,$(PRIMARY_YEARS))
REPUBLICAN_PRIMARIES = $(patsubst %,data/wards/judicial_republican_primary_%.csv,$(PRIMARY_YEARS))
GENERALS = $(patsubst %,data/wards/judicial_general_%.csv,$(GENERAL_YEARS))

DEMOGRAPHICS_PRIMARIES = $(patsubst %,data/demographics/ward_%_primary.geojson,$(PRIMARY_YEARS))
DEMOGRAPHICS_GENERALS = $(patsubst %,data/demographics/ward_%_general.geojson,$(GENERAL_YEARS))

CSVS = $(DEMOCRATIC_PRIMARIES) $(REPUBLICAN_PRIMARIES) $(GENERALS) \
           $(subst .geojson,.csv,$(DEMOGRAPHICS_PRIMARIES)) \
           $(subst .geojson,.csv,$(DEMOGRAPHICS_GENERALS))

.PHONY : all
all : $(CSVS) $(DEMOGRAPHICS_PRIMARIES) $(DEMOGRAPHICS_GENERALS)

.PHONY: generals
generals: $(GENERALS)

data/demographics/%.csv : data/demographics/%.geojson
	cat $< | python scripts/demo_to_csv.py > $@

data/wards/%.csv : data/precincts/%.csv
	csvsql -y 5 --query 'select * from (select "WARD",sum("REGISTERED VOTERS") AS "REGISTERED VOTERS",sum("BALLOTS CAST") as "BALLOTS CAST" from (select DISTINCT "WARD","PRECINCT","REGISTERED VOTERS","BALLOTS CAST" from $*) t GROUP BY "WARD") wards INNER JOIN (select "WARD","RACE","CANDIDATE",sum("VOTES") as "VOTES" from $* GROUP BY "WARD","RACE","CANDIDATE") races using ("WARD")' $< > $@

data/precincts/judicial_democratic_primary_%.csv : 
	python scripts/boe.py $< --year=$* --type=primary --party=dem > $@

data/precincts/judicial_republican_primary_%.csv : 
	python scripts/boe.py $< --year=$* --type=primary --party=rep > $@

data/precincts/judicial_general_%.csv : 
	python scripts/boe.py $< --year=$* --type=general > $@

data/demographics/ward_2020_primary.geojson : wards_2012.geojson
	cat $< | python scripts/demo.py 2018 > $@

data/demographics/ward_2018_primary.geojson : wards_2012.geojson
	cat $< | python scripts/demo.py 2018 > $@

data/demographics/ward_2018_general.geojson : wards_2012.geojson
	cat $< | python scripts/demo.py 2018 > $@

data/demographics/ward_2016_primary.geojson : wards_2012.geojson
	cat $< | python scripts/demo.py 2016 > $@

data/demographics/ward_2016_general.geojson : wards_2012.geojson
	cat $< | python scripts/demo.py 2016 > $@

data/demographics/ward_2014_primary.geojson : wards_2012.geojson
	cat $< | python scripts/demo.py 2014 > $@

data/demographics/ward_2014_general.geojson : wards_2012.geojson
	cat $< | python scripts/demo.py 2014 > $@

data/demographics/ward_2012_primary.geojson : wards_2002.geojson
	cat $< | python scripts/demo.py 2012 > $@

data/demographics/ward_2012_general.geojson : wards_2012.geojson
	cat $< | python scripts/demo.py 2012 > $@

data/demographics/ward_2010_primary.geojson : wards_2002.geojson
	cat $< | python scripts/demo.py 2010 > $@

data/demographics/ward_2010_general.geojson : wards_2002.geojson
	cat $< | python scripts/demo.py 2010 > $@

data/demographics/ward_2008_primary.geojson : wards_2002.geojson
	cat $< | python scripts/demo.py 2010 > $@

data/demographics/ward_2008_general.geojson : wards_2002.geojson
	cat $< | python scripts/demo.py 2010 > $@

data/demographics/ward_2006_primary.geojson : wards_2002.geojson
	cat $< | python scripts/demo.py 2010 > $@

data/demographics/ward_2006_general.geojson : wards_2002.geojson
	cat $< | python scripts/demo.py 2010 > $@	

data/demographics/ward_2004_primary.geojson : wards_2002.geojson
	cat $< | python scripts/demo_sf1.py 2000 > $@

data/demographics/ward_2004_general.geojson : wards_2002.geojson
	cat $< | python scripts/demo_sf1.py 2000 > $@
 
data/demographics/ward_2002_primary.geojson : wards_1998.geojson
	cat $< | python scripts/demo_sf1.py 2000 > $@

data/demographics/ward_2002_general.geojson : wards_2002.geojson
	cat $< | python scripts/demo_sf1.py 2000 > $@	

data/demographics/ward_2000_primary.geojson : wards_1998.geojson
	cat $< | python scripts/demo_sf1.py 2000 > $@

data/demographics/ward_2000_general.geojson : wards_1998.geojson
	cat $< | python scripts/demo_sf1.py 2000 > $@	

wards_1998.geojson : ward1998.shp
	ogr2ogr -f GeoJSON -t_srs crs:84 $@ $<

%.shp : %.zip
	unzip $<
	touch $@

ward1998.zip : 
	wget -O $@ "https://www.lib.uchicago.edu/e/collections/maps/ward1998.zip"

wards_2012.geojson :
	wget -O $@ "https://data.cityofchicago.org/api/geospatial/sp34-6z76?method=export&format=GeoJSON"

wards_2002.geojson :
	wget -O $@ "https://data.cityofchicago.org/api/geospatial/xt4z-bnwh?method=export&format=GeoJSON"
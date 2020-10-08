# chicago-judicial-elections
Chicago Judicial Elections

Data and Scripts to Acquire Data for Chicago Judicial Elections

## Data Manifest
- [./data/wards/*.csv](./data/wards) : CSV Spreadsheets of Judicial Race Results at the Ward Level
- [./data/demographics/*.csv](./data/demographics) : CSV Spreadsheets of Racial, Ethnic, and Income Demographics at Ward Level for Each Election
- [./data/demographics/*.geojson](./data/demographics) : GeoJSON Files of Racial, Ethnic, and Income Demographics at Ward Level for Each Election. Good for mapping


## Sources
The election results all come for the [Chicago Board of Elections](https://chicagoelections.gov/en/election-results.html).

The Census data comes from the US Census's data API. We use the nearest available year for each election.


Census data sources
| year | Census Source    |
|------|------------------|
| 2020 | 2019 ACS, 5 year |
| 2018 | 2018 ACS, 5 year |
| 2016 | 2016 ACS, 5 year |
| 2014 | 2014 ACS, 5 year |
| 2012 | 2012 ACS, 5 year |
| 2010 | 2010 ACS, 5 year |
| 2008 | 2010 ACS, 5 year |
| 2006 | 2010 ACS, 5 year |
| 2004 | 2000 SF1         |
| 2002 | 2000 SF1         |
| 2000 | 2000 SF1         |

## Methodology

See this [project for the methodology of calculating the demographics for each ward](https://github.com/datamade/ward-demographics#methodology).


## To Run
### System requirements
- ogr2ogr
- python3
- make
- wget

### Install
```bash
> pip install -r requirements.txt
```

### Build data
```bash
> make all
```

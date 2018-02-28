# azure-cosmos-graph

CosmosDB Graph Database example.

Start with the IMDb datasets, wrangle them to a smaller size, load them into
the CosmosDB/GraphDB, and search for the nth degrees of Kevin Bacon and others.

## CosmosDB Provisioning

In Azure Portal, provision a CosmosDB with the Graph API.

Capture its keys in portal, and set these as environment variables:
```
AZURE_COSMOSDB_GRAPH1_ACCT=xxx
AZURE_COSMOSDB_GRAPH1_KEY=yyy
```

## IMDb Data

You can download the data from here:

- http://www.imdb.com/interfaces/
- https://datasets.imdbws.com

### Raw Data

This is the list of the downloaded zipped and unzipped files, with their sizes
```
 511846598 Feb 27 10:52 name.basics.tsv
 165971634 Feb 25 05:17 name.basics.tsv.gz
 174443242 Feb 27 10:52 title.akas.tsv
  52330181 Feb 25 05:17 title.akas.tsv.gz
 409681927 Feb 27 10:50 title.basics.tsv
  87696341 Feb 25 05:17 title.basics.tsv.gz
  81236137 Feb 27 10:52 title.episode.tsv
  17665426 Feb 26 05:19 title.episode.tsv.gz
1208052497 Feb 27 10:52 title.principals.tsv
 241072882 Feb 26 05:19 title.principals.tsv.gz
  13764321 Feb 27 10:52 title.ratings.tsv
   3998762 Feb 26 05:19 title.ratings.tsv.gz
```

Also set the IMDB_DATA_DIR environment variable to point to the root directory
for your data; this can and should be a separate directory from this code repository.
```
IMDB_DATA_DIR=/Users/cjoakim/Downloads/imdb
```

The imdb/ directory will contain a raw/ and /processed subdirectories;
the downloaded and unzipped files go into raw/

### Data Wrangling

See wrangle.sh and wrangle.py; they produce the following output files.

### Output Data

#### movies.csv
```
id|title
tt0012349|The Kid
tt0013442|Nosferatu
tt0015864|The Gold Rush
tt0017136|Metropolis
tt0017925|The General
tt0021749|City Lights
tt0022100|M
tt0024216|King Kong
tt0025316|It Happened One Night
```

#### movies.json
```
{
  ...
  "tt0087182": "Dune",
  "tt0087277": "Footloose",
  "tt0087332": "Ghostbusters",
  "tt0087363": "Gremlins",
  "tt0087469": "Indiana Jones and the Temple of Doom",
  ...
}
```

#### people.json
```
  ...
  "nm0000102": {
    "birth": "1958",
    "movies": {
      "tt0087277": "Footloose",
      "tt0164052": "Hollow Man",
      "tt0327056": "Mystic River"
    },
    "name": "Kevin Bacon",
    "nid": "nm0000102",
    "prof": "actor,producer,soundtrack",
    "titles": [
      "tt0087277",
      "tt0164052",
      "tt0327056"
    ]
  },
  ...
  "nm0000210": {
    "birth": "1967",
    "movies": {
      "tt0100405": "Pretty Woman",
      "tt0125439": "Notting Hill",
      "tt0195685": "Erin Brockovich",
      "tt0376541": "Closer"
    },
    "name": "Julia Roberts",
    "nid": "nm0000210",
    "prof": "actress,producer,soundtrack",
    "titles": [
      "tt0376541",
      "tt0195685",
      "tt0100405",
      "tt0125439"
    ]
  }
```

## Loading the Data CosmosDB

See cosmos_load.py and cosmos_load.sh



## Querying CosmosDB

See cosmos_query.py and cosmos_query.sh


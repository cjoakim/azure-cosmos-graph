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

## Gremlin-Python and Apache TinkerPop

Apache TinkerPop is a graph computing framework for both graph databases (OLTP)
and graph analytic systems (OLAP).

- https://pypi.python.org/pypi/gremlinpython/3.2.7
- http://tinkerpop.apache.org
- http://tinkerpop.apache.org/docs/current/reference/#gremlin-python

## Loading the Data CosmosDB

See cosmos_graph.py and cosmos_graph.sh

### Queries


```
IDs:
footloose=tt0087277
prettywoman=tt0100405
kevinbacon=nm0000102
juliaroberts=nm0000210
richardgere=nm0000152

g.V()                           select all
g.V().count()                   count all
g.V().has('label','movie')
g.V().has('label','movie').has('id','tt0100405')        find movie with the given id (Pretty Woman)
g.V().has('label','movie').has('title','Pretty Woman')  find movie with the given title

g.V().has('label','person').has('id','nm0000210')       find person with the given id (Julia Roberts)
g.V().has('label','person').has('name','Julia Roberts') find person with the given name

g.V().has('label','person').has('id','nm0000102')       find person with the given id (Kevin Bacon)

Execute query: g.V("nm0000210").both().as('v').project('vertex', 'edges').by(select('v')).by(bothE().fold())
Execute query: g.V("tt0100405").both().as('v').project('vertex', 'edges').by(select('v')).by(bothE().fold())
Execute query: g.V("nm0000210").both().as('v').project('vertex', 'edges').by(select('v')).by(bothE().fold())
Execute query: g.V("nm0000102").both().as('v').project('vertex', 'edges').by(select('v')).by(bothE().fold())

wip:
g.V().has('id','nm0000210').inE('in')  <- returns reasonable json
g.V().has('label','person').has('id','nm0000210').out().values('id')

g.V('nm0000210').repeat(out()).until(has('id', 'nm0000152')).path()
g.V('nm0000210').repeat(out()).hasLabel('person').until(has('id', 'nm0000152')).path()
g.V('nm0000210').out('in').hasLabel('movie').out('has').hasLabel('person').values('nm0000152')
```

```
Update Thomas                          : "g.V('thomas').property('age', 44)"

Traversals:
Get all persons older than 40          : "g.V().hasLabel('person').has('age', gt(40)).values('firstName', 'age')",
Get all persons and their first name   : "g.V().hasLabel('person').values('firstName')",
Get all persons sorted by first name   : "g.V().hasLabel('person').order().by('firstName', incr).values('firstName')",
Get all persons that Thomas knows      : "g.V('thomas').out('knows').hasLabel('person').values('firstName')",
People known by those who Thomas knows : "g.V('thomas').out('knows').hasLabel('person').out('knows').hasLabel('person').values('firstName')",
Get the path from Thomas to Robin"     : "g.V('thomas').repeat(out()).until(has('id', 'robin')).path()"
```

## Querying CosmosDB

See cosmos_graph.py and cosmos_graph.sh

## Six_Degrees_of_Kevin_Bacon

https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon

"...in a January 1994 interview with Premiere magazine discussing the film The River Wild, mentioned that "he had worked with everybody in Hollywood or someone who’s worked with them."[1] On April 7, 1994, a lengthy newsgroup thread headed "Kevin Bacon is the Center of the Universe" appeared.  Four Albright College students: Craig Fass, Christian Gardner, Brian Turtle, and Mike Ginelli created the game early in 1994."

It rests on the assumption that anyone involved in the Hollywood film industry can be linked through their film roles to Bacon within six steps.



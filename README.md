# azure-cosmos-graph

CosmosDB Graph Database example.

Start with the IMDb datasets, wrangle them to a smaller size, load them into
the CosmosDB/GraphDB, and search for the nth degrees of Kevin Bacon and others.

## CosmosDB Provisioning

In Azure Portal, provision a CosmosDB with the Graph API.

10,000 RUs -> Estimated spend (USD): $0.80 hourly / $19.20 daily.

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
- http://gremlindocs.spmallette.documentup.com (TinkerPop 2.x)
- http://tinkerpop.apache.org (Download Gremlin console)
- https://docs.microsoft.com/en-us/azure/cosmos-db/create-graph-gremlin-console

## Loading the Data CosmosDB

See cosmos_graph.py and cosmos_graph.sh

Log output:
```
insert_movie_vertices; count: 2518

```

### Queries


```
IDs:
footloose=tt0087277
pretty_woman=tt0100405
kevin_bacon=nm0000102
julia_roberts=nm0000210
richardgere=nm0000152
john_lithgow=nm0001475
tom_hanks=nm0000158
lori_singer=nm0001742
john_malkovich=
dustin_hoffman=nm0000163


g.V()                           select all
g.V().count()                   count all
g.V().has('label','movie')
g.V().has('label','movie').has('id','tt0100405')        find movie with the given id (Pretty Woman)
g.V().has('label','movie').has('title','Pretty Woman')  find movie with the given title
g.V('tt0100405')                                        Pretty Woman
g.V('tt0087277')                                        Footloose

g.V().has('label','person').has('id','nm0000210')       find person with the given id (Julia Roberts)
g.V('nm0000210')                                        simpler way to find Julia Roberts
g.V().has('label','person').has('name','Julia Roberts') find person with the given name

g.V().has('label','person').has('id','nm0000102')       find person with the given id (Kevin Bacon)

g.V('nm0000210').out('knows').values('name').path()

g.V('nm0000210').bothE().where(otherV().hasId('nm0000152'))
g.V('nm0000210').bothE().where(otherV().hasId('nm0000152')).path()
g.V('nm0000210').bothE().where(otherV().hasId('nm0001742'))
g.V('nm0000152').bothE().where(otherV().hasId('nm0000163'))

Execute query: g.V("nm0000210").both().as('v').project('vertex', 'edges').by(select('v')).by(bothE().fold())
Execute query: g.V("tt0100405").both().as('v').project('vertex', 'edges').by(select('v')).by(bothE().fold())
Execute query: g.V("nm0000210").both().as('v').project('vertex', 'edges').by(select('v')).by(bothE().fold())
Execute query: g.V("nm0000102").both().as('v').project('vertex', 'edges').by(select('v')).by(bothE().fold())

wip:

:> g.V('nm0000210')
:> g.V('nm0000210').outE('in').inV().hasLabel('person')
:> g.V().hasLabel('person').has('firstName', 'Thomas').outE('knows').inV().hasLabel('person')

g.V(1).bothE().where(otherV().hasId(2))
g.V().has('label','person').has('name','Julia Roberts').bothE().where(otherV().hasId('nm0000152'))

g.V().group().by().by(bothE().count()) # Degree centrality is a measure of the number of edges associated to each vertex.


g.V('nm0000210').inE() <- returns reasonable json
g.V('nm0000210').inE().until(has('id', 'nm0000152'))

g.V('nm0000210').out('Pretty Woman')  # works

g.V().as('nm0000210').repeat(out().simplePath()).times(2).where(out().as('nm0000152')).path()

g.V('nm0000210').repeat(out()).until(has('id', 'nm0000158')).path()

spec = "g.V('{}').addE('{}').to(g.V('{}'))"
g.V('nm0000210').addE('knows').to(g.V('nm0000102'))

spec = "g.V('{}').addE('knows', 'title', '{}').to(g.V('{}'))"
g.V('nm0000210').addE('knows', 'title', 'xxx').to(g.V('nm0000102'))

g.V('nm0000210').has('label','person').has('id','nm0000102').out().values('id')

g.V('nm0000210').repeat(out()).until(has('id', 'nm0000152')).path()
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

Monday 3/6 2pm attempt:
```
insert_movie_vertices:    g.addV('movie').property('name', 'Pretty Woman').property('id', 'tt0100405')
insert_people_vertices:   g.addV('person').property('name', 'Julia Roberts').property('id', 'nm0000210')
insert_people_vertices:   g.addV('person').property('name', 'Richard Gere').property('id', 'nm0000152')
person-in-movie edge:     g.V().hasLabel('person').has('id', 'nm0000210').addE('in').to(g.V().hasLabel('movie').has('id', 'tt0100405'))
person-knows-person edge: g.V().hasLabel('person').has('id', 'nm0000152').addE('knows').to(g.V().hasLabel('person').has('id', 'nm0000210'))


g.V('nm0000210').repeat(out()).until(has('id', 'nm0000152')).path()
g.V().hasLabel('person').has('id', 'nm0000210').repeat(out()).until(has('id', 'nm0000152')).path()

g.V('nm0000152').repeat(out()).until(has('id', 'nm0000210')).path()  # has results
g.V('nm0000210').repeat(out()).until(has('id', 'nm0000152')).path()  # has no results!

g.V('nm0000152').repeat(out().simplePath()).until(hasId('nm0000210')).path().count(local)
```

## Gremlin Console

- See this tutorial: https://docs.microsoft.com/en-us/azure/cosmos-db/create-graph-gremlin-console
- Dowload the 3.2.7 client from here: http://tinkerpop.apache.org/downloads.html
- Unzip the apache-tinkerpop-gremlin-console-3.2.7-bin.zip
- Edit file conf/remote-secure.yaml and enter your CosmosDB values as shown below:
- In bash terminal, execte bin/gremlin.sh to start the Gremlin Console
- In the console, run the following to connect to CosmosDB
  gremlin> :remote connect tinkerpop.server conf/remote-secure.yaml
- Execute queries prefixed with ':>', examples below


```
gremlin> :> g.V().count()
==>6507

gremlin> :> g.V('nm0000102')
==>[id:nm0000102,label:person,type:vertex,properties:[name:[[id:34dd09d4-4146-401d-8439-566b8db34940,value:Kevin Bacon]]]]

gremlin> :> g.V('nm0000210')
==>[id:nm0000210,label:person,type:vertex,properties:[name:[[id:a3a7350c-854f-4f28-9f70-630a5c99de92,value:Julia Roberts]]]]

gremlin> :> g.V('nm0000152')
==>[id:nm0000152,label:person,type:vertex,properties:[name:[[id:7949640e-be51-4a09-af6f-aab5b5761029,value:Richard Gere]]]]

gremlin> :> g.V('tt0100405')
==>[id:tt0100405,label:movie,type:vertex,properties:[title:[[id:b7869705-e32c-4801-ba87-be361511ee21,value:Pretty Woman]]]]

gremlin> :> g.V('nm0000210').outE().inV().hasLabel('movie')
==>[id:tt0376541,label:movie,type:vertex,properties:[title:[[id:db412101-b34a-4097-9cb3-5dac26adb41a,value:Closer]]]]
==>[id:tt0195685,label:movie,type:vertex,properties:[title:[[id:c1763d68-b5d7-4b76-8fb7-5b6a745c26fd,value:Erin Brockovich]]]]
==>[id:tt0100405,label:movie,type:vertex,properties:[title:[[id:b7869705-e32c-4801-ba87-be361511ee21,value:Pretty Woman]]]]
==>[id:tt0125439,label:movie,type:vertex,properties:[title:[[id:e25b5183-da90-4892-8778-235c4c11746d,value:Notting Hill]]]]

gremlin> :> g.V('nm0000152').outE().inV()

gremlin> :> g.V('nm0000152').outE().inV()
==>[id:tt0299658,label:movie,type:vertex,properties:[title:[[id:2d1c6214-79e7-43b0-861e-5cfb209f4dcb,value:Chicago]]]]
==>[id:tt0100405,label:movie,type:vertex,properties:[title:[[id:b7869705-e32c-4801-ba87-be361511ee21,value:Pretty Woman]]]]


:> g.V('nm0000210').outE().inV().hasLabel('person')
```


Example conf/remote-secure.yaml file:
```
hosts: [cjoakim-cosmos-graph1.gremlin.cosmosdb.azure.com]
port: 443
username: /dbs/test/colls/movies
password: h2Dwm7 ... X6nUkSw==
connectionPool: {enableSsl: true}
serializer: {className: org.apache.tinkerpop.gremlin.driver.ser.GraphSONMessageSerializerV1d0, config: { serializeResultToString: true }}
```

## Simple Manual Case

### Create Vectors and Edges

```
Create 3 Movies
g.addV('movie').property('name', 'Movie1').property('id', 'm1')
g.addV('movie').property('name', 'Movie2').property('id', 'm2')
g.addV('movie').property('name', 'Movie3').property('id', 'm3')
g.V('m1')

Create 6 People
g.addV('person').property('name', 'Adam').property('id', 'p1')
g.addV('person').property('name', 'Barbara').property('id', 'p2')
g.addV('person').property('name', 'Charles').property('id', 'p3')
g.addV('person').property('name', 'Darlene').property('id', 'p4')
g.addV('person').property('name', 'Edward').property('id', 'p5')
g.addV('person').property('name', 'Fiona').property('id', 'p6')
g.V('p1')

Create Edges from People-to-Movies
g.V('p1').addE('in').to(g.V('m1'))
g.V('p2').addE('in').to(g.V('m1'))
g.V('p3').addE('in').to(g.V('m1'))
g.V('p4').addE('in').to(g.V('m2'))
g.V('p5').addE('in').to(g.V('m2'))
g.V('p6').addE('in').to(g.V('m3'))

overlaps
g.V('p3').addE('in').to(g.V('m2'))
g.V('p6').addE('in').to(g.V('m2'))
g.V('m1')
g.V('m2')
g.V('m3')

g.V().hasLabel('person').has('name', 'Adam').property('movies', '["Movie1"]')
g.V().hasLabel('person').has('name', 'Fiona').property('movies', '["Movie2", "Movie3"]')

Create Edges from people-to-people - this the results of this syntax are questionable
g.V('p1').addE('knows').to(g.V('p2'))
g.V('p1').addE('knows').to(g.V('p3'))
g.V('p2').addE('knows').to(g.V('p3'))
g.V('p4').addE('knows').to(g.V('p5'))
g.V('p3').addE('knows').to(g.V('p4'))
g.V('p3').addE('knows').to(g.V('p5'))
g.V('p6').addE('knows').to(g.V('p4'))
g.V('p6').addE('knows').to(g.V('p5'))

This person-to-person syntax works better
g.V().hasLabel('person').has('id', 'p1').addE('knows').to(g.V().hasLabel('person').has('id', 'p2'))
g.V().hasLabel('person').has('id', 'p1').addE('knows').to(g.V().hasLabel('person').has('id', 'p3'))
g.V().hasLabel('person').has('id', 'p2').addE('knows').to(g.V().hasLabel('person').has('id', 'p3'))
g.V().hasLabel('person').has('id', 'p4').addE('knows').to(g.V().hasLabel('person').has('id', 'p5'))
g.V().hasLabel('person').has('id', 'p3').addE('knows').to(g.V().hasLabel('person').has('id', 'p4'))
g.V().hasLabel('person').has('id', 'p3').addE('knows').to(g.V().hasLabel('person').has('id', 'p5'))
g.V().hasLabel('person').has('id', 'p6').addE('knows').to(g.V().hasLabel('person').has('id', 'p4'))
g.V().hasLabel('person').has('id', 'p6').addE('knows').to(g.V().hasLabel('person').has('id', 'p5'))
```

### Query

```
g.V().hasLabel('person')

g.V().hasLabel('person').has('name', 'Adam').outE('knows').inV().hasLabel('person')

Get the path from Thomas to Robin"
g.V('p1').repeat(out()).until(has('id', 'p6')).path()
```


## Querying CosmosDB

See cosmos_graph.py and cosmos_graph.sh

## Six_Degrees_of_Kevin_Bacon

https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon

"...in a January 1994 interview with Premiere magazine discussing the film The River Wild, mentioned that "he had worked with everybody in Hollywood or someone who’s worked with them."[1] On April 7, 1994, a lengthy newsgroup thread headed "Kevin Bacon is the Center of the Universe" appeared.  Four Albright College students: Craig Fass, Christian Gardner, Brian Turtle, and Mike Ginelli created the game early in 1994."

It rests on the assumption that anyone involved in the Hollywood film industry can be linked through their film roles to Bacon within six steps.



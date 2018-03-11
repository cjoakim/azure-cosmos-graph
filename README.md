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

TODO - revisit

## Gremlin-Python and Apache TinkerPop

Apache TinkerPop is a graph computing framework for both graph databases (OLTP)
and graph analytic systems (OLAP).

- https://pypi.python.org/pypi/gremlinpython/3.2.7
- http://tinkerpop.apache.org/docs/3.2.7/recipes/
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

### Some of the Actors

- Footloose https://www.youtube.com/watch?v=AFQaVbIPOWk


### Queries




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
username: /dbs/dev/colls/movies
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


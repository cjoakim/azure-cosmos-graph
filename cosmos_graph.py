"""
Usage:
  python cosmos_graph.py drop_graph test movies
  python cosmos_graph.py create_drop_and_load_queries test movies
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# Chris Joakim, Microsoft, 2018/03/07

import csv, json, os, sys, time, traceback

# gremlin_python lib is Gremlin-Python for Apache TinkerPop
# see http://tinkerpop.apache.org
# see https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-support


from gremlin_python.driver import client

from docopt import docopt

from pysrc.joakim import config
from pysrc.joakim import values

VERSION='2018/03/06'
FOOTLOOSE='tt0087277'
PRETTYWOMAN='tt0100405'
KEVINBACON='nm0000102'
JULIAROBERTS='nm0000210'

class Main:

    def __init__(self):
        self.start_time = time.time()
        self.args = sys.argv
        self.c = config.Config()
        self.favorites = values.Favorites()
        self.queries = list()
        self.sleep_time = 0.25
        self.submit_query = False

    def execute(self):
        if len(sys.argv) > 3:
            func = sys.argv[1].lower()
            db   = sys.argv[2].lower()
            coll = sys.argv[3].lower()
            print('function: {}'.format(func))

            if func == 'drop_graph':
                self.drop_graph(db, coll)

            elif func == 'create_drop_and_load_queries':
                self.create_drop_and_load_queries(db, coll)

            elif func == 'query':
                self.query(db, coll)
            else:
                self.print_options('Error: invalid function: {}'.format(func))
        else:
            self.print_options('Error: no function argument provided.')

    def create_client(self, db, coll):
        # Get a database connection from the Gremlin Server.
        endpoint = self.c.cosmosdb_gremlin_url()
        username = self.c.cosmosdb_gremlin_username(db, coll)
        password = self.c.cosmosdb_key()
        print('endpoint: {}'.format(endpoint))
        print('username: {}'.format(username))
        print('password: {}'.format(password))
        self.gremlin_client = client.Client(endpoint, 'g', username=username, password=password)
        time.sleep(1)
        print(self.gremlin_client) # <gremlin_python.driver.client.Client object at 0x109305b38>

    def drop_graph(self, db, coll):
        print('drop_graph - db {} coll: {}'.format(db, coll))
        query = 'g.V().drop()'
        self.create_client(db, coll)
        self.execute_query(query, 10)

    def execute_query(self, query, sleep_time=0.25):
        if query:
            self.queries.append(query)
            if self.submit_query:
                print('execute_query: {}  # {}'.format(query, len(self.queries)))
                callback = self.gremlin_client.submitAsync(query)
                if callback.result() is None:
                    print("query not successful")
                time.sleep(sleep_time)
            else:
                print('create_query: {}  # {}'.format(query, len(self.queries)))

    def create_drop_and_load_queries(self, db, coll):
        print('create_drop_and_load_queries START')
        infile1 = self.c.movies_json_filename()
        infile2 = self.c.people_json_filename()
        self.movies = json.load(open(self.c.movies_json_filename()))
        self.people = json.load(open(self.c.people_json_filename()))
        self.queries.append('g.V().drop()')
        self.create_movie_vertices()
        self.create_people_vertices()
        self.create_edges()

        outfile = self.c.drop_and_load_queries_txt_filename()
        with open(outfile, "w", newline="\n") as out:
            for line in self.queries:
                out.write(line + "\n")
            print('file written: {}'.format(outfile))

        print('create_drop_and_load_queries COMPLETE')

    def create_movie_vertices(self):
        movies_ids = sorted(self.movies.keys())
        print('create_movie_vertices; count: {}'.format(len(movies_ids)))
        spec = "g.addV('movie').property('id', '{}').property('title', '{}')"

        for idx, mid in enumerate(movies_ids):
            title = self.scrub_str(self.movies[mid])
            query = spec.format(mid, title)
            self.queries.append(query)

    def create_people_vertices(self):
        people_ids = sorted(self.people.keys())
        print('create_people_vertices; count: {}'.format(len(people_ids)))
        spec = "g.addV('person').property('id', '{}').property('name', '{}')"

        for idx, pid in enumerate(people_ids):
            person = self.people[pid]
            name   = self.scrub_str(person['name'])
            query  = spec.format(pid, name)
            print('create_people_vertices: {}  # {}'.format(query, idx))
            self.queries.append(query)

    def create_edges(self):
        people_ids = sorted(self.people.keys())
        #spec = "g.V('{}').addE('in').to(g.V('{}'))"
        spec = "g.V('{}').addE('in').to(g.V('{}')).property('title', '{}')"

        # First add the person-in-movie Edges:
        for idx, pid in enumerate(people_ids):
            person = self.people[pid]
            name   = self.scrub_str(person['name'])
            titles = person['titles']

            for mid in titles:
                title = self.scrub_str(self.movies[mid])
                query = spec.format(pid, mid, title)
                self.queries.append(query)

        # Next add the person-knows-person Edges:
        people_edges = json.load(open(self.c.people_edges_json_filename()))
        concat_keys  = sorted(people_edges.keys())
        #spec = "g.V('{}').addE('knows').to(g.V('{}'))"
        spec = "g.V('{}').addE('knows').to(g.V('{}')).property('title', '{}')"

        for idx, key in enumerate(concat_keys):
            title = people_edges[key].replace("'", '')
            pair  = key.split(':')
            # create the edge from person 1 to person 2
            query = spec.format(pair[0], pair[1], title)
            self.queries.append(query)

        for idx, key in enumerate(concat_keys):
            title = people_edges[key].replace("'", '')
            pair  = key.split(':')
            # create the edge from person 2 to person 1
            query = spec.format(pair[1], pair[0], title)
            self.queries.append(query)

    def execute_drop_and_load_queries(self):
        pass

    def query(self, db, coll):
        # python cosmos_graph.py query test movies count
        # python cosmos_graph.py query test movies movie   tt0087277
        # python cosmos_graph.py query test movies movie   footloose
        # python cosmos_graph.py query test movies movie_e footloose
        # python cosmos_graph.py query test movies movie   pretty_woman
        # python cosmos_graph.py query test movies edges   pretty_woman
        # python cosmos_graph.py query test movies person  julia_roberts
        # python cosmos_graph.py query test movies person  diane_lane
        # python cosmos_graph.py query test movies path    julia_roberts richard_gere
        # python cosmos_graph.py query test movies path    richard_gere julia_roberts
        # python cosmos_graph.py query test movies path    kevin_bacon julia_roberts
        # python cosmos_graph.py query test movies path    kevin_bacon richard_gere
        # python cosmos_graph.py query test movies v2v     julia_roberts
        # python cosmos_graph.py query test movies knows1  julia_roberts
        # python cosmos_graph.py query test movies in      tt0086927

        self.create_client(db, coll)
        qname = sys.argv[4].lower()
        query = None

        if qname == 'count':
            query = 'g.V().count()'

        elif qname == 'movie':
            arg = sys.argv[5].lower()
            id  = self.favorites.translate_to_id(arg)
            query = "g.V().has('label','movie').has('id','{}')".format(id)

        elif qname == 'movie_e':
            arg = sys.argv[5].lower()
            id  = self.favorites.translate_to_id(arg)
            query = "g.V('{}').both().as('v').project('vertex', 'edges').by(select('v')).by(bothE().fold())".format(id)

        elif qname == 'person':
            arg = sys.argv[5].lower()
            id  = self.favorites.translate_to_id(arg)
            query = "g.V().has('label','person').has('id','{}')".format(id)

        elif qname == 'person_e':
            arg = sys.argv[5].lower()
            id  = self.favorites.translate_to_id(arg)
            query = "g.V('{}').both().as('v').project('vertex', 'edges').by(select('v')).by(bothE().fold())".format(id)

        elif qname == 'edges':
            arg = sys.argv[5].lower()
            id  = self.favorites.translate_to_id(arg)
            query = "g.V('{}').both().as('v').project('vertex', 'edges').by(select('v')).by(bothE().fold())".format(id)

        elif qname == 'v2v':
            arg = sys.argv[5].lower()
            id  = self.favorites.translate_to_id(arg)
            query = "g.V('{}').bothE().inV()".format(id)

        elif qname == 'knows':
            id1 = self.favorites.translate_to_id(sys.argv[5].lower())
            #query = "g.V('{}').out('knows').out('knows').out('knows')".format(id1)
            #query = "g.V('{}').repeat(out('knows')).times(1)".format(id1)
            query = "g.V('{}').out('knows')".format(id1)

        elif qname == 'in':
            id1 = self.favorites.translate_to_id(sys.argv[5].lower())
            #query = "g.V('{}').out('knows').out('knows').out('knows')".format(id1)
            #query = "g.V('{}').repeat(out('knows')).times(1)".format(id1)
            query = "g.V('{}').out('in')".format(id1)

        elif qname == 'path':
            arg1 = sys.argv[5].lower()
            arg2 = sys.argv[6].lower()
            id1  = self.favorites.translate_to_id(arg1)
            id2  = self.favorites.translate_to_id(arg2)
            query = "g.V('{}').bothE().where(otherV().hasId('{}')).path()".format(id1, id2)

        if query:
            print('qname: {}'.format(qname))
            print('query: {}'.format(query))

            callback = self.gremlin_client.submitAsync(query)
            if callback.result() is not None:
                #print(type(callback.result()))  # <class 'gremlin_python.driver.resultset.ResultSet'>
                print('--- result_below ---')
                rlist = callback.result().one() # <class 'list'>
                jstr = json.dumps(rlist, sort_keys=False, indent=2)
                print(jstr)
            else:
                print("query returned None")
        else:
            print('invalid args')

    def scrub_str(self, s):
        return s.replace("'", '')

    def print_options(self, msg):
        print(msg)
        arguments = docopt(__doc__, version=VERSION)
        print(arguments)


Main().execute()

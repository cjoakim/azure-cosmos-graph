"""
Usage:
  python cosmos_graph.py drop_graph test movies
  python cosmos_graph.py drop_and_load test movies
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# Chris Joakim, Microsoft, 2018/03/01

import csv, json, os, sys, time, traceback

# gremlin_python lib is Gremlin-Python for Apache TinkerPop
# see http://tinkerpop.apache.org
from gremlin_python.driver import client

from docopt import docopt

from pysrc.joakim import config


VERSION='2018/03/01a'
FOOTLOOSE='tt0087277'
PRETTYWOMAN='tt0100405'
KEVINBACON='nm0000102'
JULIAROBERTS='nm0000210'

class Main:

    def __init__(self):
        self.start_time = time.time()
        self.args = sys.argv
        self.c = config.Config()

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

    def execute(self):
        if len(sys.argv) > 3:
            func = sys.argv[1].lower()
            db   = sys.argv[2].lower()
            coll = sys.argv[3].lower()
            print('function: {}'.format(func))

            if func == 'drop_graph':
                self.drop_graph(db, coll)

            elif func == 'drop_and_load':
                self.drop_and_load(db, coll)

            elif func == 'count_query':
                self.count_query(db, coll)

            elif func == 'query2':
                self.query2(db, coll)

            elif func == 'query3':
                self.query3(db, coll)

            elif func == 'ad_hoc':
                self.ad_hoc(db, coll)
            else:
                self.print_options('Error: invalid function: {}'.format(func))
        else:
            self.print_options('Error: no function argument provided.')

    def ad_hoc(self, db, coll):
        print('ad_hoc')
        self.create_client(db, coll)

    def drop_and_load(self, db, coll):
        print('drop_and_load')
        infile1 = self.c.movies_json_filename()
        infile2 = self.c.people_json_filename()
        self.movies = json.load(open(self.c.movies_json_filename()))
        self.people = json.load(open(self.c.people_json_filename()))
        self.max_load = 20000
        self.sleep_time = 0.5
        self.do_inserts = True

        self.drop_graph(db, coll)
        self.insert_movie_vertices()
        self.insert_people_vertices()
        self.insert_edges();

    def drop_graph(self, db, coll):
        query = 'g.V().drop()'
        print('drop_graph; query: {}'.format(query))
        self.create_client(db, coll)

        callback = self.gremlin_client.submitAsync(query)
        if callback.result() is not None:
            print("graph dropped!")
        else:
            print("graph NOT dropped!")

    def insert_movie_vertices(self):
        # example: g.addV('movie').property('id', 'tt0083658').property('title', 'Blade Runner')
        movies_ids = sorted(self.movies.keys())
        print('insert_movie_vertices; count: {}'.format(len(movies_ids)))

        for idx, id in enumerate(movies_ids):
            title = self.scrub_str(self.movies[id])
            spec  = "g.addV('movie').property('id', '{}').property('title', '{}')"
            query = spec.format(id, title)
            print('insert_movie_vertices: {}  # {} {}'.format(query, idx, self.do_inserts))
            if self.do_inserts:
                if idx < self.max_load:
                    callback = self.gremlin_client.submitAsync(query)
                    if callback.result() is not None:
                        print("movie vertex loaded: " + query)
                    else:
                        print("movie vertex NOT loaded!")
                    time.sleep(self.sleep_time)

    def insert_people_vertices(self):
        # example: g.addV('person').property('id', 'nm0000442').property('name', 'Rutger Hauer')
        people_ids = sorted(self.people.keys())
        print('insert_people_vertices; count: {}'.format(len(people_ids)))

        for idx, pid in enumerate(people_ids):
            person = self.people[pid]
            name  = self.scrub_str(person['name'])
            spec  = "g.addV('person').property('id', '{}').property('name', '{}')"
            query = spec.format(pid, name)
            print('insert_people_vertices: {}  # {} {}'.format(query, idx, self.do_inserts))
            if self.do_inserts:
                if idx < self.max_load:
                    callback = self.gremlin_client.submitAsync(query)
                    if callback.result() is not None:
                        print("person vertex loaded: " + query)
                    else:
                        print("person vertex NOT loaded!")
                    time.sleep(self.sleep_time)

    def insert_edges(self):
        print('insert_edges')
        # examples:
        # g.V('nm0000102').addE('in').to(g.V('tt0087277'))  # Kevin Bacon in Footloose
        # g.V('tt0087277').addE('has').to(g.V('nm0000102')) # Footloose has Kevin Bacon
        #
        # "nm0000102": {
        # "birth": "1958",
        # "movies": {
        #   "tt0087277": "Footloose",
        #   "tt0164052": "Hollow Man",
        #   "tt0327056": "Mystic River"
        # },
        # "name": "Kevin Bacon",
        # "nid": "nm0000102",
        # "prof": "actor,producer,soundtrack",
        # "titles": [
        #   "tt0087277",
        #   "tt0164052",
        #   "tt0327056"]
        # },
        people_ids = sorted(self.people.keys())
        count = 0
        for idx, pid in enumerate(people_ids):
            person = self.people[pid]
            name   = self.scrub_str(person['name'])
            titles = person['titles']

            # Add the person-in-movie Edges
            spec  = "g.V('{}').addE('in').to(g.V('{}'))"
            for mid in titles:
                query = spec.format(pid, mid)
                count = count + 1
                print('insert_edges; p in m: {}  # {} {}'.format(query, count, self.do_inserts))
                if self.do_inserts:
                    if idx < self.max_load:
                        callback = self.gremlin_client.submitAsync(query)
                        if callback.result() is not None:
                            print("edge loaded: " + query)
                        else:
                            print("edge NOT loaded!")
                        time.sleep(self.sleep_time)

            # Add the person-knows-person Edges
            people_edges = json.load(open(self.c.people_edges_json_filename()))
            concat_keys = sorted(people_edges.keys())
            spec = "g.V('{}').addE('knows').to(g.V('{}'))"
            for key in concat_keys:
                pair = key.split(':')
                pid1, pid2 = pair[0], pair[1]
                query = spec.format(pid1, pid2)
                callback = self.gremlin_client.submitAsync(query)
                if callback.result() is not None:
                    print("person-knows-person loaded: " + query)
                else:
                    print("person-knows-person NOT loaded!")
                time.sleep(self.sleep_time)

            # Add the movie-has-person Edges
            if False:
                spec  = "g.V('{}').addE('has').to(g.V('{}'))"
                for mid in titles:
                    query = spec.format(mid, pid)
                    count = count + 1
                    print('insert_edges; m has p: {}  # {} {}'.format(query, count, self.do_inserts))
                    if self.do_inserts:
                        if idx < self.max_load:
                            callback = self.gremlin_client.submitAsync(query)
                            if callback.result() is not None:
                                print("edge loaded: " + query)
                            else:
                                print("edge NOT loaded!")
                            time.sleep(self.sleep_time)

    def count_query(self, db, coll):
        self.create_client(db, coll)
        query = 'g.V().count()'
        print('count_query: {}'.format(query))
        query
        callback = self.gremlin_client.submitAsync(query)
        if callback.result() is not None:
            print(callback.result().one())
        else:
            print("query returned None")

    def query2(self, db, coll):
        self.create_client(db, coll)
        query = "g.V().has('label','movie').has('id','tt0100405')"
        print('query2: {}'.format(query))
        query
        callback = self.gremlin_client.submitAsync(query)
        # callback.result() is an instance of gremlin_python.driver.resultset.ResultSet
        # all() returns a <Future at 0x1085fbe80 state=pending>
        if callback.result() is not None:
            print(type(callback.result()))  # <class 'gremlin_python.driver.resultset.ResultSet'>
            rlist = callback.result().one() # <class 'list'>
            print(type(rlist))
            for idx, item in enumerate(rlist):
                print('{} {}'.format(idx, item))
        else:
            print("query returned None")

    def query3(self, db, coll):
        self.create_client(db, coll)
        query = "g.V('nm0000210').both().as('v').project('vertex', 'edges').by(select('v')).by(bothE().fold())"
        print('query3: {}'.format(query))
        query
        callback = self.gremlin_client.submitAsync(query)
        # callback.result() is an instance of gremlin_python.driver.resultset.ResultSet
        # all() returns a <Future at 0x1085fbe80 state=pending>
        if callback.result() is not None:
            print(type(callback.result()))  # <class 'gremlin_python.driver.resultset.ResultSet'>
            rlist = callback.result().one() # <class 'list'>
            jstr = json.dumps(rlist, sort_keys=False, indent=2)
            print(jstr)
        else:
            print("query returned None")

    def scrub_str(self, s):
        return s.replace("'", '')

    def print_options(self, msg):
        print(msg)
        arguments = docopt(__doc__, version=VERSION)
        print(arguments)


Main().execute()

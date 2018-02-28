"""
Usage:
  python cosmos_graph.py drop_graph test movies
  python cosmos_graph.py drop_and_load test movies
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# Chris Joakim, Microsoft, 2018/02/28

import csv, json, os, sys, time, traceback

# gremlin_python lib is Gremlin-Python for Apache TinkerPop
# see http://tinkerpop.apache.org
from gremlin_python.driver import client

from docopt import docopt

from pysrc.joakim import config


VERSION='2018/02/28a'
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
        print('insert_movie_vertices')
        movies_ids = sorted(self.movies.keys())
        for idx, id in enumerate(movies_ids):
            title = self.scrub_str(self.movies[id])
            spec  = "g.addV('movie').property('id', '{}').property('title', '{}')"
            query = spec.format(id, title)
            print('insert_movie_vertices: {}  # {}'.format(query, self.do_inserts))
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
        print('insert_people_vertices')
        people_ids = sorted(self.people.keys())
        for idx, pid in enumerate(people_ids):
            person = self.people[pid]
            name  = self.scrub_str(person['name'])
            spec  = "g.addV('person').property('id', '{}').property('name', '{}')"
            query = spec.format(pid, name)
            print('insert_people_vertices: {}  # {}'.format(query, self.do_inserts))
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
        for idx, pid in enumerate(people_ids):
            person = self.people[pid]
            name   = self.scrub_str(person['name'])
            titles = person['titles']

            # Add the person-in-movie Edges
            spec  = "g.V('{}').addE('in').to(g.V('{}'))"
            for mid in titles:
                query = spec.format(pid, mid)
                print('insert_edges; p in m: {}  # {}'.format(query, self.do_inserts))
                if self.do_inserts:
                    if idx < self.max_load:
                        callback = self.gremlin_client.submitAsync(query)
                        if callback.result() is not None:
                            print("edge loaded: " + query)
                        else:
                            print("edge NOT loaded!")
                        time.sleep(self.sleep_time)

            # Add the movie-has-person Edges
            spec  = "g.V('{}').addE('has').to(g.V('{}'))"
            for mid in titles:
                query = spec.format(mid, pid)
                print('insert_edges; m has p: {}  # {}'.format(query, self.do_inserts))
                if self.do_inserts:
                    if idx < self.max_load:
                        callback = self.gremlin_client.submitAsync(query)
                        if callback.result() is not None:
                            print("edge loaded: " + query)
                        else:
                            print("edge NOT loaded!")
                        time.sleep(self.sleep_time)



    def scrub_str(self, s):
        return s.replace("'", '')

    def print_options(self, msg):
        print(msg)
        arguments = docopt(__doc__, version=VERSION)
        print(arguments)


Main().execute()
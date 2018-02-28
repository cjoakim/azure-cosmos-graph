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

    def drop_graph(self, db, coll):
        query = 'g.V().drop()'
        print('drop_graph; query: {}'.format(query))
        self.create_client(db, coll)

        callback = self.gremlin_client.submitAsync(query)
        if callback.result() is not None:
            print("graph dropped!")
        else:
            print("graph NOT dropped!")

    def drop_and_load(self, db, coll):
        print('drop_and_load')
        # self.create_client(db, coll)
        # self.drop_graph()
        self.insert_movie_vertices()
        self.insert_people_vertices()
        self.insert_edges();

    def insert_movie_vertices(self):
        print('insert_movie_vertices')
        infile = self.c.movies_json_filename()
        movies = json.load(open(infile))
        print(movies)

    def insert_people_vertices(self):
        print('insert_people_vertices')

    def insert_edges(self):
        print('insert_edges')

    def print_options(self, msg):
        print(msg)
        arguments = docopt(__doc__, version=VERSION)
        print(arguments)


Main().execute()

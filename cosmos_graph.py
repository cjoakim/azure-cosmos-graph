"""
Usage:
  python cosmos_graph.py drop_graph dev movies
  python cosmos_graph.py create_load_queries dev movies
  python cosmos_graph.py execute_load_queries dev movies
  python cosmos_graph.py query dev movies countv
  python cosmos_graph.py query dev movies movie    tt0087277
  python cosmos_graph.py query dev movies movie    footloose
  python cosmos_graph.py query dev movies movie    pretty_woman
  python cosmos_graph.py query dev movies person   julia_roberts
  python cosmos_graph.py query dev movies person   nm0001742
  python cosmos_graph.py query dev movies edges    footloose
  python cosmos_graph.py query dev movies edges    julia_roberts
  python cosmos_graph.py query dev movies vertices julia_roberts
  python cosmos_graph.py query dev movies knows    kevin_bacon
  python cosmos_graph.py query dev movies in       julia_roberts
  python cosmos_graph.py query dev movies path     richard_gere julia_roberts
  python cosmos_graph.py query dev movies path     richard_gere kevin_bacon
  python cosmos_graph.py query dev movies path     richard_gere richard_gere
  python cosmos_graph.py capture_gremlin_queries_for_doc dev movies
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# Chris Joakim, Microsoft, 2018/03/11

import csv, json, os, sys, time, traceback
import arrow

# gremlin_python lib is Gremlin-Python for Apache TinkerPop
# see http://tinkerpop.apache.org
# see https://docs.microsoft.com/en-us/azure/cosmos-db/gremlin-support


from gremlin_python.driver import client

from docopt import docopt

from pysrc.joakim import config
from pysrc.joakim import values

VERSION='2018/03/11'
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
        self.default_sleep_time = 0.5
        self.submit_query = False
        self.load_queries = list()
        self.load_idx = 0

    def execute(self):
        if len(sys.argv) > 3:
            func = sys.argv[1].lower()
            db   = sys.argv[2].lower()
            coll = sys.argv[3].lower()
            print('function: {}'.format(func))

            if func == 'drop_graph':
                self.drop_graph(db, coll)

            elif func == 'create_load_queries':
                self.create_load_queries(db, coll)

            elif func == 'execute_load_queries':
                self.execute_load_queries(db, coll)

            elif func == 'query':
                self.query(db, coll)

            elif func == 'capture_gremlin_queries_for_doc':
                self.capture_gremlin_queries_for_doc()

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
        #print('password: {}'.format(password))
        self.gremlin_client = client.Client(endpoint, 'g', username=username, password=password)
        time.sleep(5)

    def create_load_queries(self, db, coll):
        print('create_load_queries START')
        infile1 = self.c.movies_json_filename()
        infile2 = self.c.people_json_filename()
        self.movies = json.load(open(self.c.movies_json_filename()))
        self.people = json.load(open(self.c.people_json_filename()))
        self.create_movie_vertices()
        self.create_people_vertices()
        self.create_edges()

        outfile = self.c.load_queries_txt_filename()
        with open(outfile, "w", newline="\n") as out:
            for line in self.queries:
                out.write(line + "\n")
            print('file written: {}'.format(outfile))

        print('create_load_queries COMPLETE')

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
            self.queries.append(query)

    def create_edges(self):
        people_ids = sorted(self.people.keys())

        # First add the person-in-movie Edges:
        spec = "g.V('{}').addE('in').to(g.V('{}')).property('title', '{}')"
        for idx, pid in enumerate(people_ids):
            person = self.people[pid]
            name   = self.scrub_str(person['name'])
            titles = person['titles']
            #print('pid: {} titles: {}'.format(pid, titles))
            for mid in titles:
                title = self.scrub_str(self.movies[mid])
                query = spec.format(pid, mid, title)
                self.queries.append(query)

        # Next add the person-knows-person-in-movie Edges:
        people_edges = json.load(open(self.c.people_edges_json_filename()))
        concat_keys  = sorted(people_edges.keys())
        spec = "g.V('{}').addE('knows').to(g.V('{}')).property('title', '{}').property('mid', '{}')"

        for idx, key in enumerate(concat_keys):
            # the keys look like this: "nm0000152:nm0000178:The Cotton Club:tt0087089"
            quad  = key.split(':')
            title = quad[2].replace("'", '')
            query = spec.format(quad[0], quad[1], title, quad[3])
            self.queries.append(query)

    def drop_graph(self, db, coll):
        print('drop_graph - db {} coll: {}'.format(db, coll))
        query = 'g.V().drop()'
        self.create_client(db, coll)
        self.execute_query(query, 10)

    def execute_query(self, query, t=None):
        if query:
            callback = self.gremlin_client.submitAsync(query)
            if callback.result() is None:
                print("query not successful")
            if t:
                time.sleep(t)
            else:
                time.sleep(self.default_sleep_time)

    def execute_load_queries(self, db, coll):
        infile  = self.c.load_queries_txt_filename()
        self.load_queries = list()

        self.drop_graph(db, coll)

        with open(infile, 'rt') as f:
            for idx, line in enumerate(f):
                self.load_queries.append(line.strip())

        print('{} load_queries loaded from file {}'.format(len(self.load_queries, infile)))
        self.load_loop(0)  # initiate the recursive loop

        # for idx, q in enumerate(queries):
        #     print('execute_query: {}  # {}'.format(q, idx))
        #     self.execute_query(q, self.default_sleep_time)

    def load_loop(self, idx):
        if idx < len(self.load_queries):
            query = self.load_queries[idx]
            epoch1, epoch2 = None, None
            if query:
                epoch1 = arrow.utcnow().timestamp
                print('load_loop idx: {} epoch: {} query: {}'.format(idx, epoch1, query))
                callback = self.gremlin_client.submitAsync(query)
                if callback.result() is None:
                    epoch2 = arrow.utcnow().timestamp
                    print('QUERY_NOT_SUCCESSFUL; elapsed: {}'.format(epoch2 - epoch1))
                    time.sleep(self.default_sleep_time)
                    self.load_loop(idx + 1)  # <-- recursively call this function
                else:
                    print('query_successful; elapsed: {}'.format(epoch2 - epoch1))
                    time.sleep(self.default_sleep_time)
                    self.load_loop(idx + 1)  # <-- recursively call this function
        else:
            print('load_loop completed at index {}'.format(idx))

    def capture_gremlin_queries_for_doc(self):
        queries_dir = 'queries'
        for dir_name, subdirs, file_names in os.walk(queries_dir):
            for file_name in file_names:
                fname = '{}/{}'.format(queries_dir, file_name)
                qname = file_name.split('.')[0]
                with open(fname, 'rt') as f:
                    for idx, line in enumerate(f):
                        if 'query: ' in line:
                            print('')
                            print(qname)
                            print(line.strip())

    def query(self, db, coll):
        self.create_client(db, coll)
        qname = sys.argv[4].lower()
        query = None

        if qname == 'countv':
            query = 'g.V().count()'

        elif qname == 'movie':
            arg = sys.argv[5].lower()
            id  = self.favorites.translate_to_id(arg)
            query = "g.V().has('label','movie').has('id','{}')".format(id)

        elif qname == 'person':
            arg = sys.argv[5].lower()
            id  = self.favorites.translate_to_id(arg)
            query = "g.V().has('label','person').has('id','{}')".format(id)

        elif qname == 'edges':
            arg = sys.argv[5].lower()
            id  = self.favorites.translate_to_id(arg)
            #query = "g.V('{}').both().as('v').project('vertex', 'edges').by(select('v')).by(bothE().fold())".format(id)
            query = "g.V('{}').bothE()".format(id)

        elif qname == 'vertices':
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

        # elif qname == 'path_orig':
        #     arg1 = sys.argv[5].lower()
        #     arg2 = sys.argv[6].lower()
        #     id1  = self.favorites.translate_to_id(arg1)
        #     id2  = self.favorites.translate_to_id(arg2)
        #     query = "g.V('{}').bothE().where(otherV().hasId('{}')).path()".format(id1, id2)

        elif qname == 'path':
            arg1 = sys.argv[5].lower()
            arg2 = sys.argv[6].lower()
            id1  = self.favorites.translate_to_id(arg1)
            id2  = self.favorites.translate_to_id(arg2)
            query = "g.V('{}').repeat(out().simplePath()).until(hasId('{}')).path().limit(3)".format(id1, id2)

        if query:
            print('qname: {}'.format(qname))
            print('query: {}'.format(query))

            callback = self.gremlin_client.submitAsync(query)
            if callback.result() is not None:
                #print(type(callback.result()))  # <class 'gremlin_python.driver.resultset.ResultSet'>
                print('--- result_below ---')
                data = dict()
                r = callback.result().one()
                data['qname'] = qname
                data['query'] = query
                data['result_count'] = len(r)
                data['result'] = r
                jstr = json.dumps(data, sort_keys=False, indent=2)
                print(jstr)

                outfile = 'tmp/query_{}_{}.json'.format(qname, arrow.utcnow().timestamp)
                with open(outfile, "w") as out:
                    out.write(jstr)
                    print('--- result_above ---')
                    print('file written: {}'.format(outfile))
        else:
            print('invalid args')

    def scrub_str(self, s):
        return s.replace("'", '')

    def print_options(self, msg):
        print(msg)
        arguments = docopt(__doc__, version=VERSION)
        print(arguments)


Main().execute()

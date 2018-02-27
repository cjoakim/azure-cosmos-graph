import json
import os


class Config:

    def __init__(self):
        self.values = {}
        try:
            with open(self.config_filename(), 'r') as f:
                self.values = json.loads(f.read())
        except:
            print("Exception in Config constructor on file: " + self.config_filename())

    def config_filename(self):
        return 'config.json'

    def cosmosdb_acct(self):
        return os.environ['AZURE_COSMOSDB_GRAPH1_ACCT']

    def cosmosdb_uri(self):
        return os.environ['AZURE_COSMOSDB_GRAPH1_URI']

    def cosmosdb_gremlin_url(self):
        acct = self.cosmosdb_acct()
        return "wss://{}.gremlin.cosmosdb.azure.com:443/".format(acct)

    def cosmosdb_key(self):
        return os.environ['AZURE_COSMOSDB_GRAPH1_KEY']

    def data_dir(self):
        return os.environ['IMDB_DATA_DIR']
        # IMDB_DATA_DIR=/Users/cjoakim/Downloads/imdb

    def data_filename(self, basename):
        return '{}/{}'.format(self.data_dir(), basename)
        # name.basics.tsv
        # title.akas.tsv
        # title.basics.tsv
        # title.episode.tsv
        # title.principals.tsv
        # title.ratings.tsv

    def top_ratings_csv_filename(self):
        return self.data_filename('top_ratings.csv')

    def top_movies_csv_filename(self):
        return self.data_filename('top_movies.csv')

    def load(self):
        try:
            with open(json_filename, 'r') as json_file:
                self.values = json.loads(json_file.read())
        except:
            print("Exception in Config.load on file: " + json_filename)
            self.values = {}
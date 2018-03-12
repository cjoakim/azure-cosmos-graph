import json
import os

# Chris Joakim, Microsoft, 2018/03/11


class D3Util:

    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.lines = list()

        with open(self.infile, 'rt') as f:
            for idx, line in enumerate(f):
                self.lines.append(line)

    def load_query_results(self):
        try:
            with open(json_filename, 'r') as json_file:
                self.values = json.loads(json_file.read())
        except:
            print("Exception in Config.load on file: " + json_filename)
            self.values = {}

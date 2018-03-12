import json
import os

# Chris Joakim, Microsoft, 2018/03/11


class D3Util:

    def __init__(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile
        self.lines = list()
        self.qname = None
        self.query = None
        self.json_lines = list()
        self.results_obj = None

        # collect the lines of the query-result infile
        with open(self.infile, 'rt') as f:
            for idx, line in enumerate(f):
                self.lines.append(line)

        # scan the input lines
        in_json = False
        for line in self.lines:
            if line.startswith('qname: '):
                tokens = line.split()
                self.qname = tokens[1]
            if line.startswith('query: '):
                tokens = line.split()
                self.query = tokens[1]
            if line.startswith('--- result_above ---'):
                in_json = False
            if in_json:
                self.json_lines.append(line)
            if line.startswith('--- result_below ---'):
                in_json = True

        jstr = ''.join(self.json_lines)
        self.results_obj = json.loads(jstr)

    def load_query_results(self):
        try:
            with open(json_filename, 'r') as json_file:
                self.values = json.loads(json_file.read())
        except:
            print("Exception in Config.load on file: " + json_filename)
            self.values = {}

import json
import os

# Chris Joakim, Microsoft, 2018/03/12


class D3Util:

    def __init__(self, json_infile, json_outfile='d3/graph1.json'):
        print('D3Util#__init__: {}'.format(json_infile))
        self.infile = json_infile
        self.outfile = json_outfile
        self.qname = None
        self.query = None
        self.results_obj = None
        self.graph_obj = {}

        with open(self.infile, 'r') as f:
            self.results_obj = json.loads(f.read())

        self.parse()

        jstr = json.dumps(self.graph_obj, indent=2)
        with open(self.outfile, 'wt') as f:
            f.write(jstr)
            print('file written: {}'.format(self.outfile))

    def parse(self):
        pass

import json
import os

# Chris Joakim, Microsoft, 2018/03/12


class D3Util:

    def __init__(self, json_infile, json_outfile='d3/graph.json'):
        print('D3Util#__init__: {}'.format(json_infile))
        self.infile = json_infile
        self.outfile = json_outfile
        self.results_obj = None
        self.graph_obj = {}
        self.nodes = list() # array of dict objects
        self.node_ids = dict()
        self.links = list() # array of dict objects
        self.graph_obj['nodes'] = self.nodes
        self.graph_obj['links'] = self.links

        with open(self.infile, 'r') as f:
            self.results_obj = json.loads(f.read())

        self.graph_obj['qname'] = self.results_obj['qname']
        self.graph_obj['query'] = self.results_obj['query']

        if '_path_' in self.infile:
            self.parse_path()

        jstr = json.dumps(self.graph_obj, indent=2)
        with open(self.outfile, 'wt') as f:
            f.write(jstr)
            print('file written: {}'.format(self.outfile))

    def parse_path(self):
        paths = self.results_obj['result']

        # First create the Nodes (Vertices)
        for path_idx, path in enumerate(paths):
            objects = path['objects']
            obj_count = len(objects)
            for obj_idx, obj in enumerate(objects):
                next_obj_idx = obj_idx + 1
                if next_obj_idx < obj_count:
                    next_obj = objects[next_obj_idx]
                    self.add_node(obj, next_obj)
                else:
                    self.add_node(obj)

        # Next create the Links (Edges)
        for path_idx, path in enumerate(paths):
            objects = path['objects']
            obj_count = len(objects)
            for obj_idx, obj in enumerate(objects):
                next_obj_idx = obj_idx + 1
                if next_obj_idx < obj_count:
                    next_obj = objects[next_obj_idx]
                    self.add_link(obj, next_obj, path_idx)

    def add_node(self, obj, next_obj=None):
        id = obj['id']
        if id not in self.node_ids:
            d = dict()
            d['id'] = id
            d['name'] = obj['properties']['name'][0]['value']
            d['label'] = obj['label']
            self.node_ids[id] = d
            self.nodes.append(d)

    def add_link(self, obj, next_obj, path_idx):
        d = dict()
        d['source'] = obj['id']
        d['target'] = next_obj['id']
        d['type']   = 'knows, path {}'.format(path_idx + 1)
        d['since']  = ''
        self.links.append(d)

        # "objects": [
        #   {
        #     "id": "nm0001742",
        #     "label": "person",
        #     "type": "vertex",
        #     "properties": {
        #       "name": [
        #         {
        #           "id": "fb444d04-c856-4142-ae57-8cc94b5ba5e4",
        #           "value": "Lori Singer"
        #         }
        #       ]
        #     }
        #   },

        # nodes:
        # {
        #   "name": "Peter",
        #   "label": "Person",
        #   "id": 1
        # },

        # links:
        # {
        #   "source": 1,
        #   "target": 2,
        #   "type": "KNOWS",
        #   "since": 2010
        # },

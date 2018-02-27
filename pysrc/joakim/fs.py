# Chris Joakim, Microsoft, 2018/02/27

import csv
import json

from joakim import config
from joakim import fixed
from joakim import fs


class FSUtil(object):

    def __init__(self):
        pass

    def read_csvfile(self, infile, delim=','):
        rows = list()
        with open(infile) as csvfile:
            reader = csv.reader(csvfile, delimiter=delim)
            for row in reader:
                rows.append(row)
        return rows

    def read_csvfile_into_objects(self, infile, delim=','):
        objects = list()  # return a list of dicts
        with open(infile) as csvfile:
            reader = csv.reader(csvfile, delimiter=delim)
            headers = None
            for idx, row in enumerate(reader):
                if idx == 0:
                    headers = row
                else:
                    if len(row) == len(headers):
                        obj = dict()
                        for field_idx, field_name in enumerate(headers):
                            key = field_name.strip().lower()
                            obj[key] = row[field_idx].strip()
                        objects.append(obj)
        return objects

    def read_text_file(self, infile):
        lines = list()
        with open(infile, 'rt') as f:
            for idx, line in enumerate(f):
                lines.append(line.strip())
        return lines

    def read_json_file(self, infile):
        return json.load(open(infile))

    def write_csvfile(self, outfile, rows):
        print('write_csvfile: {}'.format(outfile))
        with open(outfile, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in rows:
                writer.writerow(row)

    def write_obj_as_json_file(self, outfile, obj):
        txt = json.dumps(obj, sort_keys=True, indent=2)
        with open(outfile, 'wt') as f:
            f.write(txt)
        print("file written: " + outfile)

    def write_text_file(self, outfile, txt):
        with open(outfile, 'wt') as f:
            f.write(txt)
        print("file written: " + outfile)

    def write_lines(self, outfile, lines):
        with open(outfile, "w", newline="\n") as out:
            for line in lines:
                out.write(line + "\n")
            print('file written: {}'.format(outfile))

    def get_property_file_fields(self):
        c = config.Config()
        infile = c.property_list_field_spec_file()
        lines  = self.read_text_file(infile)
        fields = list()
        for idx, line in enumerate(lines):
            if idx > 0:
                fs = fixed.FieldSpec(line)
                fields.append(fs)
        return fields



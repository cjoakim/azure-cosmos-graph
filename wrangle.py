"""
Usage:
  python wrangle.py scan_title_basics
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# Chris Joakim, Microsoft, 2018/02/27

import csv
import json
import os
import sys
import time
import traceback

from docopt import docopt

from pysrc.joakim import config


VERSION='2018/02/27a'


class Main:

    def __init__(self):
        self.start_time = time.time()
        self.args = sys.argv
        self.c = config.Config()
        self.roles = self.selected_roles()

    def execute(self):
        if len(sys.argv) > 1:
            f = sys.argv[1].lower()
            print('function: {}'.format(f))

            if f == 'extract_top_ratings':
                self.extract_top_ratings()

            elif f == 'extract_top_movies':
                self.extract_top_movies()

            elif f == 'extract_people':
                self.extract_people()

            elif f == 'scan2':
                pass
            else:
                self.print_options('Error: invalid function: {}'.format(f))
        else:
            self.print_options('Error: no function argument provided.')

    def extract_top_ratings(self):
        # Identify and extract the top (movie) ratings with at least n-votes
        infile = self.c.data_filename('title.ratings.tsv')
        outfile = self.c.top_ratings_csv_filename()
        min_votes = self.c.extract_min_votes()
        selected  = dict()
        row_count = 0

        with open(infile) as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            for row in reader:
                # OrderedDict([('tconst', 'tt0000001'), ('averageRating', '5.8'), ('numVotes', '1349')])
                try:
                    row_count = row_count + 1
                    votes = int(row['numVotes'])
                    if votes > min_votes:
                        id = row['tconst']
                        selected[id] = votes
                    # if row_count < 10:
                    #     print(row)
                    #     print(row['tconst'])
                except:
                    print('exception on row {} {}'.format(row_count, row))

        print("extract_top_ratings - selected count: {}".format(len(selected.keys())))

        with open(outfile, "w", newline="\n") as out:
            out.write("id|votes\n")
            for id in sorted(selected.keys()):
                votes = selected[id]
                line  = '{}|{}'.format(id.strip(), votes)
                out.write(line + "\n")
            print('file written: {}'.format(outfile))

        elapsed_time = time.time() - self.start_time
        print('lines_read: {}  elapsed: {}'.format(row_count, elapsed_time))
        # lines_read: 4832632  elapsed: 25.33212375640869

    def extract_top_movies(self):
        infile = self.c.data_filename('title.basics.tsv')
        outfile1 = self.c.top_movies_csv_filename()
        outfile2 = self.c.top_movies_json_filename()
        selected = dict()
        row_count = 0
        top_rated = self.load_top_ratings()

        with open(infile) as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            for row in reader:
                # OrderedDict([('tconst', 'tt0000009'), ('titleType', 'movie'), ('primaryTitle', 'Miss Jerry'),
                # ('originalTitle', 'Miss Jerry'), ('isAdult', '0'), ('startYear', '1894'), ('endYear', '\\N'),
                # ('runtimeMinutes', '45'), ('genres', 'Romance')])
                try:
                    row_count = row_count + 1
                    id = row['tconst']
                    if id in top_rated:
                        if 'movie' == row['titleType']:
                            if '0' == row['isAdult']:
                                title = row['primaryTitle']
                                selected[id] = title
                                #print('selected top_rated item {} {}'.format(id, title))
                except:
                    print('exception on row {} {}'.format(row_count, row))

        print("extract_top_movies - selected count: {}".format(len(selected.keys())))

        with open(outfile1, "w", newline="\n") as out:
            out.write("id|title\n")
            for id in sorted(selected.keys()):
                title = selected[id]
                line  = '{}|{}'.format(id.strip(), title.strip())
                out.write(line + "\n")
            print('file written: {}'.format(outfile1))

        jstr = json.dumps(selected, sort_keys=True, indent=2)
        with open(outfile2, 'wt') as f:
            f.write(jstr)
            print('file written: {}'.format(outfile2))

    def extract_people(self):
        # wc -l name.basics.tsv -> 8449645 name.basics.tsv
        infile  = self.c.data_filename('name.basics.tsv')
        outfile = self.c.people_filename()
        people  = list()
        row_count = 0
        top_movies = self.load_top_movies()

        with open(infile) as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            for row in reader:
                # OrderedDict([('nconst', 'nm0000001'), ('primaryName', 'Fred Astaire'), ('birthYear', '1899'),
                # ('deathYear', '1987'), ('primaryProfession', 'soundtrack,actor,miscellaneous'),
                # ('knownForTitles', 'tt0043044,tt0050419,tt0053137,tt0072308')])
                try:
                    row_count = row_count + 1
                    prof = row['primaryProfession']

                    if self.filter_by_profession(prof):
                        #print('filter_by_profession_included: {}'.format(prof))
                        work_hits = list()
                        nid  = row['nconst']
                        name = row['primaryName']
                        prof = row['primaryProfession']
                        works = row['knownForTitles'].split(',')

                        for id in works:
                            if id in top_movies:
                                work_hits.append(id)

                        if len(work_hits) > 0:
                            hits = ','.join(work_hits)
                            line = '{}|{}|{}|{}'.format(nid, name, prof, hits)
                            people.append(line)
                except:
                    print('exception on row {} {}'.format(row_count, row))
                    traceback.print_exc()

        print("extract_people - selected count: {}".format(len(people)))

        with open(outfile, "w", newline="\n") as out:
            out.write("nid|name|prof|work\n")
            for person in people:
                out.write(person + "\n")
            print('file written: {}'.format(outfile))

        elapsed_time = time.time() - self.start_time
        print('lines_read: {}  elapsed: {}'.format(row_count, elapsed_time))

    # private

    def selected_roles(self):
        # This is the range of roles; but we're only extracting a subset of these:
        # actor,actress,animation_department,art_department,art_director,assistant,assistant_director,
        # camera_department,casting_department,casting_director,cinematographer,composer,costume_department,
        # costume_designer,director,editor,editorial_department,electrical_department,executive,legal,
        # location_management,make_up_department,manager,miscellaneous,music_department,producer,
        # production_department,production_designer,production_manager,publicist,script_department,
        # set_decorator,sound_department,soundtrack,special_effects,stunts,talent_agent,
        # transportation_department,visual_effects,writer

        #return 'actor,actress,director,producer'.split(',')
        return 'actor,actress'.split(',')

    def filter_by_profession(self, prof):
        professions = prof.split(',')
        for p in professions:
            if p in self.roles:
                return True
        return False

    def load_top_ratings(self):
        infile1 = self.c.top_ratings_csv_filename()
        top_rated = dict()
        row_count = 0
        with open(infile1) as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            for row in reader:
                # ['tt0000417', '34795']
                try:
                    row_count = row_count + 1
                    if row_count > 1:
                        id = row[0]
                        top_rated[id] = 0
                except:
                    print('exception on row {} {}'.format(row_count, row))
        print('loaded the top_rated; count: {}'.format(len(top_rated.keys())))
        return top_rated

    def load_top_movies(self):
        infile1 = self.c.top_movies_csv_filename()
        top_rated = dict()
        row_count = 0
        with open(infile1) as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            for row in reader:
                # ['tt0004972', 'The Birth of a Nation']
                try:
                    row_count = row_count + 1
                    if row_count > 1:
                        id, title = row[0], row[1]
                        top_rated[id] = title
                except:
                    print('exception on row {} {}'.format(row_count, row))
        print('loaded the top_movies; count: {}'.format(len(top_rated.keys())))
        return top_rated

    def print_options(self, msg):
        print(msg)
        arguments = docopt(__doc__, version=VERSION)
        print(arguments)


Main().execute()

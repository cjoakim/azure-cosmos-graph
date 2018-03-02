"""
Usage:
  python wrangle.py scan_title_basics
Options:
  -h --help     Show this screen.
  --version     Show version.
"""

# Chris Joakim, Microsoft, 2018/03/02

import csv
import json
import os
import sys
import time
import traceback

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
        self.roles = self.selected_roles()

    def execute(self):
        if len(sys.argv) > 1:
            f = sys.argv[1].lower()
            print('function: {}'.format(f))

            if f == 'extract_top_ratings':
                self.extract_top_ratings()

            elif f == 'extract_movies':
                self.extract_movies()

            elif f == 'extract_principals':
                self.extract_principals()

            elif f == 'extract_people':
                self.extract_people()

            elif f == 'derive_people_edges':
                self.derive_people_edges()

            elif f == 'scan2':
                pass
            else:
                self.print_options('Error: invalid function: {}'.format(f))
        else:
            self.print_options('Error: no function argument provided.')

    def extract_top_ratings(self):
        # Identify and extract the top (movie) ratings with at least n-votes
        infile = self.c.data_filename_raw('title.ratings.tsv')
        outfile = self.c.top_ratings_csv_filename()
        min_votes = self.c.extract_min_votes()
        min_rating = self.c.extract_min_rating()
        selected  = dict()
        row_count = 0

        with open(infile) as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            for row in reader:
                # OrderedDict([('tconst', 'tt0087277'), ('averageRating', '6.5'), ('numVotes', '58820')])
                try:
                    row_count = row_count + 1
                    votes = int(row['numVotes'])
                    rating = float(row['averageRating'])
                    id = row['tconst']
                    if votes >= min_votes:
                        if rating >= min_rating:
                            selected[id] = votes
                            if id == FOOTLOOSE:
                                print('FOOTLOOSE SELECTED: {}'.format(row))
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

    def extract_movies(self):
        infile = self.c.data_filename_raw('title.basics.tsv')
        outfile1 = self.c.movies_csv_filename()
        outfile2 = self.c.movies_json_filename()
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
                                try:
                                    ystr = row['startYear']
                                    yint = int(ystr)
                                    if yint > 1983:
                                        selected[id] = title
                                        print('selected top_rated item {} {} {}'.format(id, title, ystr))
                                except:
                                    pass
                except:
                    print('exception on row {} {}'.format(row_count, row))

        print("extract_movies - selected count: {}".format(len(selected.keys())))

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

    def extract_principals(self):
        infile   = self.c.data_filename_raw('title.principals.tsv')
        outfile1 = self.c.principals_csv_filename()
        principals = list()
        row_count = 0
        movies = self.load_movies()

        with open(infile) as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            for row in reader:
                # OrderedDict([('tconst', 'tt0000032'), ('ordering', '1'), ('nconst', 'nm3692479'),
                # ('category', 'actress'), ('job', '\\N'), ('characters', '["The dancer"]')])
                try:
                    row_count = row_count + 1
                    # if row_count < 10:
                    #     print(row)
                    id = row['tconst']
                    if id in movies:
                        role = row['category']
                        if role in self.roles:
                            nid = row['nconst']
                            line = '{}|{}|{}'.format(id, nid, role)
                            principals.append(line)
                except:
                    print('exception on row {} {}'.format(row_count, row))
                    traceback.print_exc()

        with open(outfile1, "w", newline="\n") as out:
            out.write("id|nid|role\n")
            for line in principals:
                out.write(line + "\n")
            print('file written: {}'.format(outfile1))

    def extract_people(self):
        # wc -l name.basics.tsv -> 8449645 name.basics.tsv
        infile   = self.c.data_filename_raw('name.basics.tsv')
        outfile1 = self.c.people_csv_filename()
        outfile2 = self.c.people_json_filename()
        people_list = list()
        people_dict = dict()
        row_count = 0
        principal_ids = self.unique_principal_ids()
        movies = self.load_movies()

        with open(infile) as tsvfile:
            reader = csv.DictReader(tsvfile, dialect='excel-tab')
            for row in reader:
                # OrderedDict([('nconst', 'nm0000001'), ('primaryName', 'Fred Astaire'), ('birthYear', '1899'),
                # ('deathYear', '1987'), ('primaryProfession', 'soundtrack,actor,miscellaneous'),
                # ('knownForTitles', 'tt0043044,tt0050419,tt0053137,tt0072308')])
                try:
                    row_count = row_count + 1
                    if row_count < 10:
                        print(row)
                    nid = row['nconst']
                    if nid in principal_ids:
                        # create a csv line
                        known4 = row['knownForTitles']
                        titles = self.filter_titles(movies, known4)
                        name   = row['primaryName']
                        birth  = row['birthYear']
                        prof   = row['primaryProfession']
                        line   = '{}|{}|{}|{}|{}'.format(nid, name, birth, titles, prof)
                        people_list.append(line)

                        # also create a corresponding person Object for the JSON
                        person = {}
                        person['nid']    = nid
                        person['name']   = name
                        person['birth']  = birth
                        person['prof']   = prof
                        person['titles'] = titles.split()
                        m = dict()
                        for id in titles.split():
                            mname = movies[id]
                            m[id] = mname
                        person['movies'] = m
                        people_dict[nid] = person
                except:
                    print('exception on row {} {}'.format(row_count, row))
                    traceback.print_exc()

        with open(outfile1, "w", newline="\n") as out:
            out.write("nid|name|birth|titles|profession\n")
            for line in people_list:
                out.write(line + "\n")
            print('file written: {}'.format(outfile1))

        jstr = json.dumps(people_dict, sort_keys=True, indent=2)
        with open(outfile2, 'wt') as f:
            f.write(jstr)
            print('file written: {}'.format(outfile2))

    def derive_people_edges(self):
        infile1  = self.c.movies_json_filename()
        infile2  = self.c.people_json_filename()
        infile3  = self.c.principals_csv_filename()
        outfile1 = self.c.principals_json_filename()
        outfile2 = self.c.people_edges_json_filename()
        movies = json.load(open(self.c.movies_json_filename()))
        people = json.load(open(self.c.people_json_filename()))
        people_keys = sorted(people.keys())
        print('movies: {}'.format(len(movies.keys())))
        print('people: {}'.format(len(people.keys())))
        principals, people_edges, row_count = dict(), dict(), 0

        # collect the principals dictionary, keyed by movie id, with a
        # dict as the value with title and list of people
        with open(infile3) as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            for row in reader:
                row_count = row_count + 1
                if row_count > 1:
                    prin_obj, mid, pid = None, row[0], row[1]
                    if mid in principals:
                        prin_obj = principals[mid]
                    else:
                        prin_obj = dict()
                        prin_obj['title'] = movies[mid]
                        prin_obj['people'] = list()
                    pers_obj = dict()
                    pers_obj['id'] = pid
                    pers_obj['name'] = people[pid]['name']
                    prin_obj['people'].append(pers_obj)
                    principals[mid] = prin_obj

        jstr = json.dumps(principals, sort_keys=True, indent=2)
        with open(outfile1, 'wt') as f:
            f.write(jstr)
            print('file written: {}'.format(outfile1))

        for mid in sorted(principals.keys()):
            people = principals[mid]['people']
            title  = movies[mid]
            for person1 in people:
                for person2 in people:
                    if person1['id'] != person2['id']:
                        pair = sorted([person1['id'], person2['id']])
                        concat_key = '{}:{}'.format(pair[0], pair[1])
                        people_edges[concat_key] = title

        jstr = json.dumps(people_edges, sort_keys=True, indent=2)
        with open(outfile2, 'wt') as f:
            f.write(jstr)
            print('file written: {}'.format(outfile2))

        people_edges = json.load(open(self.c.people_edges_json_filename()))
        concat_keys = sorted(people_edges.keys())
        for key in concat_keys:
            pair = key.split(':')
            print(pair)

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

    def filter_titles(self, movies, known_for):
        titles = list()
        for id in known_for.split(','):
            if id in movies:
                titles.append(id)
        return ' '.join(titles).strip()

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

    def load_movies(self):
        infile1 = self.c.movies_csv_filename()
        movies  = dict()
        row_count = 0
        with open(infile1) as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            for row in reader:
                # ['tt0004972', 'The Birth of a Nation']
                try:
                    row_count = row_count + 1
                    if row_count > 1:
                        id, title = row[0], row[1]
                        movies[id] = title
                except:
                    print('exception on row {} {}'.format(row_count, row))
        print('loaded the movies; count: {}'.format(len(movies.keys())))
        return movies

    def unique_principal_ids(self):
        infile1 = self.c.principals_csv_filename()
        principal_ids = dict()
        row_count = 0
        with open(infile1) as csvfile:
            reader = csv.reader(csvfile, delimiter='|')
            for row in reader:
                # id|nid|role
                # tt0012349|nm0088471|actor
                # tt0012349|nm0000122|actor
                try:
                    row_count = row_count + 1
                    if row_count > 1:
                        nid = row[1]
                        principal_ids[nid] = 0
                except:
                    print('exception on row {} {}'.format(row_count, row))
        print('loaded the unique_principal_ids; count: {}'.format(len(principal_ids)))
        return principal_ids

    def print_options(self, msg):
        print(msg)
        arguments = docopt(__doc__, version=VERSION)
        print(arguments)


Main().execute()

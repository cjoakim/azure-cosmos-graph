# Chris Joakim, Microsoft, 2018/03/06


class Favorites:

    def __init__(self):
        pass

    def actors_for_candidate_movies(self):
        actors = dict()
        actors['nm0000102'] = 'kevin_bacon'
        actors['nm0000113'] = 'sandra_bullock'
        actors['nm0000126'] = 'kevin_costner'
        actors['nm0000148'] = 'harrison_ford'
        actors['nm0000152'] = 'richard_gere'
        actors['nm0000158'] = 'tom_hanks'
        actors['nm0000206'] = 'keanu_reeves'
        actors['nm0000210'] = 'julia_roberts'
        actors['nm0000234'] = 'charlize_theron'
        actors['nm0177896'] = 'bradley_cooper'
        actors['nm1297015'] = 'emma_stone'
        actors['nm2225369'] = 'jennifer_lawrence'
        #actors['nm0000163'] = 'dustin_hoffman'
        #actors['nm0000456'] = 'holly_hunter'
        #actors['nm0000518'] = 'john_malkovich'
        #actors['nm0005476'] = 'hilary_swank'
        return actors

    def favorite_actors(self):
        actors = dict()
        actors['nm0000102'] = 'kevin_bacon'
        actors['nm0000113'] = 'sandra_bullock'
        actors['nm0000126'] = 'kevin_costner'
        actors['nm0000148'] = 'harrison_ford'
        actors['nm0000152'] = 'richard_gere'
        actors['nm0000158'] = 'tom_hanks'
        actors['nm0000206'] = 'keanu_reeves'
        actors['nm0000210'] = 'julia_roberts'
        actors['nm0000234'] = 'charlize_theron'
        actors['nm0177896'] = 'bradley_cooper'
        actors['nm1297015'] = 'emma_stone'
        actors['nm2225369'] = 'jennifer_lawrence'
        actors['nm0000163'] = 'dustin_hoffman'
        actors['nm0000456'] = 'holly_hunter'
        actors['nm0000518'] = 'john_malkovich'
        actors['nm0005476'] = 'hilary_swank'
        actors['nm0000178'] = 'diane_lane'
        return actors

    def favorite_movies(self):
        movies = dict()
        movies['tt0087277'] = 'footloose'
        movies['tt0100405'] = 'pretty_woman'
        movies['tt0083658'] = 'bladerunner'
        return movies

    def translate_to_id(self, name):
        for key, value in self.favorite_actors().items():
            if name == value:
                return key
        for key, value in self.favorite_movies().items():
            if name == value:
                return key
        return name

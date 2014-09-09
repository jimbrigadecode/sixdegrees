from itertools import combinations
import networkx as nx


class Bacon():
    """ Distance and Graph of Kevin Bacon network

    The distances_to_kb map was the one that was written during the interview.
    I'm using networkx as a library to perform graph functions so that the functionality is more complete.
    """
    def __init__(self):
        f = open('actors.in')
        actor_to_movies = {}
        movie_to_actors = {}
        self.graph = nx.Graph()

        current_movie = ""
        for line in f:
            if line.startswith("\t"):
                actor = line.strip()
                if actor in actor_to_movies:
                    actor_to_movies[actor].append(current_movie)
                else:
                    actor_to_movies[actor] = [current_movie]
                movie_to_actors[current_movie].append(actor)
            else:
                current_movie = line.strip()
                movie_to_actors[current_movie] = []

        for movie in movie_to_actors:
            # add an undirected edge between each comination of actors per movie with an edge attribute of that movie
            for actor_tuple in combinations(movie_to_actors[movie], 2):
                self.graph.add_edge(actor_tuple[0], actor_tuple[1], {'movie': movie})

        self.distances_to_kb = {}
        actor_queue = ['Kevin Bacon']
        distance = 1
        while actor_queue:
            next_actor_queue = []
            for current_actor in actor_queue:
                current_actor_movies = actor_to_movies[current_actor]
                for current_movie in current_actor_movies:
                    actors_in_movie = movie_to_actors[current_movie]
                    for actor_to_add in actors_in_movie:
                        if actor_to_add not in self.distances_to_kb:
                            next_actor_queue.append(actor_to_add)
                            self.distances_to_kb[actor_to_add] = distance
            actor_queue = next_actor_queue
            distance += 1

    def distance_from(self, name):
        # special case
        if name == 'Kevin Bacon':
            return 0
        elif name in self.distances_to_kb:
            return self.distances_to_kb[name]
        else:
            return "{name} not found in file".format(name=name)

    def find_path(self, name):
        if name not in self.distances_to_kb:
            return "{name} not found in file".format(name=name)

        path_str = ""
        movie_edge_attr = nx.get_edge_attributes(self.graph, 'movie')
        path = nx.shortest_path(self.graph, name, 'Kevin Bacon')
        for i in xrange(len(path)-1):
            src = path[i]
            dest = path[i+1]

            # It's an undirected graph, but I'm not sure why the edge attributes seem directed...
            # I'm checking for both ways in this case just to get around this.
            actor_tuple = (src, dest)
            if actor_tuple in movie_edge_attr:
                movie = movie_edge_attr[actor_tuple]
                path_str += "'{src}' was in '{movie}' with '{dest}'\n".format(src=src, movie=movie, dest=dest)
            else:
                actor_tuple = (dest, src)
                if actor_tuple in movie_edge_attr:
                    movie = movie_edge_attr[actor_tuple]
                    path_str += "'{src}' was in '{movie}' with '{dest}'\n".format(src=src, movie=movie, dest=dest)

        return path_str

if __name__ == '__main__':
    bacon = Bacon()

    while True:
        actor = raw_input("Enter actor name:")
        print "Distance: {}".format(bacon.distance_from(actor))
        print bacon.find_path(actor)


import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

class Graph:
    def __init__(self):
        self.adj_list = {}
        self.vertices = {}

    def add_vertex(self, name, lat, lng):
        if name not in self.adj_list:
            self.adj_list[name] = []
            self.vertices[name] = (lat, lng)

    def add_edge(self, u, v, weight):
        self.adj_list[u].append((v, weight))

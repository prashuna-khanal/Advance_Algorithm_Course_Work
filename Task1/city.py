import math

class City:
    def __init__(self, name, lat, lng, country, population):
        self.name = name
        self.lat = float(lat)
        self.lng = float(lng)
        self.country = country
        self.population = float(population) if population else 0
        self.distance = math.sqrt(self.lat**2 + self.lng**2)

    def __repr__(self):
        return f"City({self.name}, {self.country}, Pop:{self.population})"

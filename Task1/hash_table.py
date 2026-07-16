from city import City

class HashTable:
    def __init__(self, size=1000):
        self.size = size
        self.table = [[] for _ in range(self.size)]
        self.count = 0

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, city):
        index = self._hash(city.name)
        for pair in self.table[index]:
            if pair[0] == city.name:
                pair[1] = city
                return
        self.table[index].append([city.name, city])
        self.count += 1
        if self.count / self.size > 0.7:
            self._resize()

    def search(self, name):
        index = self._hash(name)
        for pair in self.table[index]:
            if pair[0] == name: return pair[1]
        return None

    def delete(self, name):
        index = self._hash(name)
        for i, pair in enumerate(self.table[index]):
            if pair[0] == name:
                del self.table[index][i]
                self.count -= 1
                return True
        return False

    def _resize(self):
        old_table = self.table
        self.size *= 2
        self.table = [[] for _ in range(self.size)]
        self.count = 0
        for chain in old_table:
            for pair in chain:
                self.insert(pair[1])

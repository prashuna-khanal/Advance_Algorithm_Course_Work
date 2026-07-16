from city import City

class MinHeap:
    def __init__(self):
        self.heap = []

    def insert(self, city):
        self.heap.append(city)
        self._heapify_up(len(self.heap) - 1)

    def extract_min(self):
        if len(self.heap) == 0: return None
        if len(self.heap) == 1: return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index].distance < self.heap[parent].distance:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up(parent)

    def _heapify_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(self.heap) and self.heap[left].distance < self.heap[smallest].distance:
            smallest = left
        if right < len(self.heap) and self.heap[right].distance < self.heap[smallest].distance:
            smallest = right
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def search(self, name):
        for c in self.heap:
            if c.name == name: return c
        return None
        
    def delete(self, name):
        for i, c in enumerate(self.heap):
            if c.name == name:
                self.heap[i] = self.heap[-1]
                self.heap.pop()
                if i < len(self.heap):
                    self._heapify_down(i)
                    self._heapify_up(i)
                break

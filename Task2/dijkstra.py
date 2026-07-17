import heapq

def dijkstra(graph, start):
    distances = {v: float('inf') for v in graph.adj_list}
    distances[start] = 0
    pq = [(0, start)]
    previous = {v: None for v in graph.adj_list}

    while pq:
        current_dist, current_v = heapq.heappop(pq)

        if current_dist > distances[current_v]:
            continue

        for neighbor, weight in graph.adj_list[current_v]:
            if weight < 0:
                continue

            distance = current_dist + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_v
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous


def get_shortest_path(previous, start, destination):
    path = []
    current = destination

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    if not path or path[0] != start:
        return []

    return path
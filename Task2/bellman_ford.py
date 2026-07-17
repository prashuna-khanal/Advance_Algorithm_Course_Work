def bellman_ford(graph, start):
    distances = {v: float('inf') for v in graph.adj_list}
    distances[start] = 0
    previous = {v: None for v in graph.adj_list}
    
    V = len(graph.adj_list)
    for _ in range(V - 1):
        for u in graph.adj_list:
            for v, weight in graph.adj_list[u]:
                if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                    distances[v] = distances[u] + weight
                    previous[v] = u
                    
    negative_cycle = False
    for u in graph.adj_list:
        for v, weight in graph.adj_list[u]:
            if distances[u] != float('inf') and distances[u] + weight < distances[v]:
                negative_cycle = True
                break
    return distances, previous, negative_cycle

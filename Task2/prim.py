import heapq

def prim_mst(graph):
    start_node = list(graph.adj_list.keys())[0]
    visited = set([start_node])
    edges = []
    mst_edges = []
    
    for neighbor, weight in graph.adj_list[start_node]:
        heapq.heappush(edges, (weight, start_node, neighbor))
        
    while edges and len(visited) < len(graph.adj_list):
        weight, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            mst_edges.append((u, v, weight))
            for neighbor, next_weight in graph.adj_list[v]:
                if neighbor not in visited:
                    heapq.heappush(edges, (next_weight, v, neighbor))
    return mst_edges

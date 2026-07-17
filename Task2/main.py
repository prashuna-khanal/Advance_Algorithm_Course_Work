from networkx.algorithms import distance_measures
from graph import Graph, haversine
import csv
import networkx as nx
import matplotlib.pyplot as plt
import os

# We are dynamically importing dijkstra, prim, and bellman_ford 
# to demonstrate that the separate files are used.
from dijkstra import *
from prim import prim_mst
from bellman_ford import bellman_ford

def load_graph_data(filepath, limit=20):
    g = Graph()
    cities = []
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            if count >= limit: break
            try:
                name = row['city']
                g.add_vertex(name, float(row['lat']), float(row['lng']))
                cities.append(name)
                count += 1
            except ValueError: pass
                
    for i in range(len(cities)):
        for j in range(len(cities)):
            if i != j:
                u, v = cities[i], cities[j]
                lat1, lng1 = g.vertices[u]
                lat2, lng2 = g.vertices[v]
                dist = haversine(lat1, lng1, lat2, lng2)
                if dist < 3000: g.add_edge(u, v, dist)
    return g

def run_task2():
    print("Loading Graph...")
    # The dataset path is relative to where it's executed, typically root
    import os
    data_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'world_cities_data.csv')
    g = load_graph_data(data_path, limit=20)
    
    start_city = list(g.vertices.keys())[0]
    
    # 1. Dijkstra
    print(f"Running Dijkstra from {start_city}...")
    distances, previous = dijkstra(g, start_city)

    reachable = {city: dist for city, dist in distances.items() if dist != float('inf')}

    destination = max(reachable, key=reachable.get)

    shortest_path = get_shortest_path(previous, start_city, destination)

    print("Shortest Path:")
    print(" -> ".join(shortest_path))
    print(f"Distance: {distances[destination]:.2f} km")
    
    # 2. Prim's MST
    print("Running Prim's MST...")
    mst_edges = prim_mst(g)
    print(f"Prim's MST built with {len(mst_edges)} edges.")
    total_weight = sum(weight for _, _, weight in mst_edges)
    print(f"Total MST Weight: {total_weight:.2f} km")
    
    # 3. Bellman-Ford with Negative Cycles
    print("Running Bellman-Ford...")
    u1, v1 = list(g.vertices.keys())[1], list(g.vertices.keys())[2]
    u2, v2 = list(g.vertices.keys())[2], list(g.vertices.keys())[3]
    u3, v3 = list(g.vertices.keys())[3], list(g.vertices.keys())[1]
    
    g.add_edge(u1, v1, -10000)
    g.add_edge(u2, v2, -10000)
    g.add_edge(u3, v3, -10000)
    
    bf_dist, bf_prev, has_neg_cycle = bellman_ford(g, start_city)
    if has_neg_cycle:
        print("Bellman-Ford successfully detected a negative weight cycle!")
    else:
        print("Bellman-Ford did not detect a negative cycle.")
        
    # Visualization logic
    output_folder = os.path.join(os.path.dirname(__file__), "..", "Visualizations")
    os.makedirs(output_folder, exist_ok=True)    
    # Draw Dijkstra Shortest Path Tree
    nx_g = nx.DiGraph()
    for v, p in previous.items():
        if p is not None:
            nx_g.add_edge(p, v, weight=round(g.adj_list[p][next(i for i, (n, w) in enumerate(g.adj_list[p]) if n == v)][1], 2))
    
    if len(nx_g.edges) > 0:
        plt.style.use('seaborn-v0_8-darkgrid')
        plt.figure(figsize=(16, 12))
        # Use geographic coordinates (longitude as x, latitude as y)
        # Determine node sizes based on degree (more connections -> larger node)
        node_sizes = [300 + 100 * nx_g.degree(node) for node in nx_g.nodes()]
        # Edge colors based on weight (lighter for lower weight)
        edges = nx_g.edges(data='weight')
        weights = [data for (_, _, data) in edges]
        max_w = max(weights) if weights else 1
        edge_colors = [plt.cm.viridis(w / max_w) for w in weights]
        # Use a force-directed layout for clearer label placement
        pos = nx.kamada_kawai_layout(nx_g)
        # Draw nodes and edges
        nx.draw_networkx_nodes(nx_g, pos, node_color='steelblue', node_size=node_sizes)
        nx.draw_networkx_edges(nx_g, pos, edge_color=edge_colors, width=2)
        # Draw node labels with a semi-transparent background
        nx.draw_networkx_labels(nx_g, pos, font_size=10, font_weight='bold',
                                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        edge_labels = nx.get_edge_attributes(nx_g, 'weight')
        nx.draw_networkx_edge_labels(nx_g, pos, edge_labels=edge_labels, font_size=8, label_pos=0.5)
        plt.title(f"Dijkstra Shortest Path Tree\nStart City: {start_city} ", fontsize=20, fontweight='bold', pad=20)
        # Create a legend for edge weight colors
        sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=min(weights, default=0), vmax=max_w))
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=plt.gca(), shrink=0.7)
        cbar.set_label('Edge Weight')
        plt.text(
            0.02,
            0.02,
            f"Destination: {destination}\n\n"
            f"Shortest Path:\n{' → '.join(shortest_path)}\n\n"
            f"Shortest Distance: {distances[destination]:.2f} km",
            transform=plt.gca().transAxes,
            fontsize=10,
            bbox=dict(
                facecolor='white',
                edgecolor='black',
                alpha=0.85,
                boxstyle='round,pad=0.5'
            )
        )
        plt.savefig(os.path.join(output_folder, "task2_dijkstra.png"), dpi=300, bbox_inches='tight')
        print("Saved ../Visualizations/task2_dijkstra.png")
        plt.close()
    
    # Draw Prim's MST
    mst_g = nx.Graph()
    for u, v, w in mst_edges:
        mst_g.add_edge(u, v, weight=round(w, 2))
        
    if len(mst_g.edges) > 0:
        plt.style.use('seaborn-v0_8-darkgrid')
        plt.figure(figsize=(16, 12))
        # Use geographic coordinates (longitude as x, latitude as y)
        pos = {node: (g.vertices[node][1], g.vertices[node][0]) for node in mst_g.nodes()}
        # Node sizes based on degree in MST
        node_sizes = [300 + 150 * mst_g.degree(node) for node in mst_g.nodes()]
        # Edge colors based on weight using a warm colormap
        edges = mst_g.edges(data='weight')
        weights = [data for (_, _, data) in edges]
        max_w = max(weights) if weights else 1
        edge_colors = [plt.cm.plasma(w / max_w) for w in weights]
        nx.draw_networkx_nodes(mst_g, pos, node_color='orange', node_size=node_sizes)
        nx.draw_networkx_edges(mst_g, pos, edge_color=edge_colors, width=2)
        nx.draw_networkx_labels(mst_g, pos, font_size=10, font_weight='bold',
                                bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
        edge_labels = nx.get_edge_attributes(mst_g, 'weight')
        nx.draw_networkx_edge_labels(mst_g, pos, edge_labels=edge_labels, font_size=8)
        plt.title(
            f"Prim's Minimum Spanning Tree\n"
            f"Start City: {start_city} | Total Weight: {total_weight:.2f} km",
            fontsize=20,
            fontweight='bold',
            pad=20
        )
        # Legend for edge weights
        import matplotlib.patches as mpatches
        sm = plt.cm.ScalarMappable(cmap='plasma', norm=plt.Normalize(vmin=min(weights, default=0), vmax=max_w))
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=plt.gca(), shrink=0.7)
        cbar.set_label('Edge Weight')
        plt.text(
            0.02,
            0.02,
            f"Total MST Weight: {total_weight:.2f} km",
            transform=plt.gca().transAxes,
            fontsize=12,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='black')
        )
        plt.savefig(
            os.path.join(output_folder, "task2_prim_mst.png"),
            dpi=300,
            bbox_inches='tight'
        )        
        print("Saved ../Visualizations/task2_prim_mst.png")
        plt.close()

if __name__ == "__main__":
    run_task2()

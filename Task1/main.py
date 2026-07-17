import csv
import math
import time
import random
import matplotlib.pyplot as plt

from city import City
from bst import BST
from avl import AVLTree
from min_heap import MinHeap
from hash_table import HashTable

# ==========================================
# Data Loading and Testing
# ==========================================
def load_data(filepath, limit=None):
    cities = []
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            if limit and count >= limit:
                break
            try:
                city = City(
                    name=row['city'],
                    lat=row['lat'],
                    lng=row['lng'],
                    country=row['country'],
                    population=row['population']
                )
                cities.append(city)
                count += 1
            except ValueError:
                continue
    return cities

def benchmark():
    dataset_sizes = [100, 1000, 10000]
    results = {
        'BST': {'insert': [], 'search': [], 'delete': []},
        'AVL': {'insert': [], 'search': [], 'delete': []},
        'Heap': {'insert': [], 'search': [], 'delete': []},
        'Hash': {'insert': [], 'search': [], 'delete': []}
    }

    import os
    data_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'world_cities_data.csv')
    all_cities = load_data(data_path, max(dataset_sizes))
    
    for size in dataset_sizes:
        print(f"Benchmarking size {size}...")
        cities = all_cities[:size]
        
        # Test BST
        bst = BST()
        start = time.perf_counter()
        for c in cities: bst.insert(c)
        results['BST']['insert'].append(time.perf_counter() - start)
        
        search_targets = [c.name for c in random.sample(cities, min(size, 100))]
        start = time.perf_counter()
        for t in search_targets: bst.search(t)
        results['BST']['search'].append((time.perf_counter() - start) / len(search_targets))
        
        start = time.perf_counter()
        for t in search_targets: bst.delete(t)
        results['BST']['delete'].append((time.perf_counter() - start) / len(search_targets))

        # Test AVL
        avl = AVLTree()
        start = time.perf_counter()
        for c in cities: avl.insert(c)
        results['AVL']['insert'].append(time.perf_counter() - start)
        
        start = time.perf_counter()
        for t in search_targets: avl.search(t)
        results['AVL']['search'].append((time.perf_counter() - start) / len(search_targets))
        
        start = time.perf_counter()
        for t in search_targets: avl.delete(t)
        results['AVL']['delete'].append((time.perf_counter() - start) / len(search_targets))

        # Test Min-Heap
        heap = MinHeap()
        start = time.perf_counter()
        for c in cities: heap.insert(c)
        results['Heap']['insert'].append(time.perf_counter() - start)
        
        start = time.perf_counter()
        for t in search_targets: heap.search(t)
        results['Heap']['search'].append((time.perf_counter() - start) / len(search_targets))
        
        start = time.perf_counter()
        for t in search_targets: heap.delete(t)
        results['Heap']['delete'].append((time.perf_counter() - start) / len(search_targets))

        # Test HashTable
        ht = HashTable()
        start = time.perf_counter()
        for c in cities: ht.insert(c)
        results['Hash']['insert'].append(time.perf_counter() - start)
        
        start = time.perf_counter()
        for t in search_targets: ht.search(t)
        results['Hash']['search'].append((time.perf_counter() - start) / len(search_targets))
        
        start = time.perf_counter()
        for t in search_targets: ht.delete(t)
        results['Hash']['delete'].append((time.perf_counter() - start) / len(search_targets))

    # Plotting
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    ops = ['insert', 'search', 'delete']
    titles = ['Insertion Time (Total for N)', 'Search Time (Per Item)', 'Delete Time (Per Item)']
    
    for i, op in enumerate(ops):
        for ds_name, metrics in results.items():
            if ds_name == 'Heap' and op in ['search', 'delete']:
                # Skip Heap O(N) operations from plots to not skew
                continue
            axs[i].plot(dataset_sizes, metrics[op], marker='o', label=ds_name)
        axs[i].set_title(titles[i])
        axs[i].set_xlabel("Dataset Size (N)")
        axs[i].set_ylabel("Time (seconds)")
        axs[i].legend()
        axs[i].grid(True)
        axs[i].set_xscale('log')
        if op != 'insert':
            axs[i].set_yscale('log')
            
    plt.tight_layout()
    plt.savefig('Visualizations/task1_performance.png')
    print("Benchmark complete. Results saved to ../Visualizations/task1_performance.png")

if __name__ == "__main__":
    benchmark()

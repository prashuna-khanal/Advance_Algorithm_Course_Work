import csv
import os
import time
import concurrent.futures
import matplotlib.pyplot as plt

# ====================== City Class ======================
class City:
    def __init__(self, name, population):
        self.name = name
        self.population = float(population) if population else 0.0

# ====================== Load Dataset ======================
def load_data(filepath, limit=10000):
    cities = []
    with open(filepath, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            if count >= limit:
                break
            try:
                cities.append(City(row["city"], row["population"]))
                count += 1
            except (ValueError, KeyError):
                continue
    return cities

# ====================== Merge ======================
def merge(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i].population <= right[j].population:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

# ====================== Sequential Merge Sort ======================
def sequential_merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = sequential_merge_sort(arr[:mid])
    right = sequential_merge_sort(arr[mid:])
    return merge(left, right)

# ====================== Parallel Version (Stable Chunk Method) ======================
def parallel_merge_sort(arr, executor, num_workers):
    if len(arr) <= 1:
        return arr

    # Divide into chunks
    chunk_size = max(500, len(arr) // (num_workers * 2))
    chunks = [arr[i:i + chunk_size] for i in range(0, len(arr), chunk_size)]
    
    # Sort all chunks in parallel
    sorted_chunks = list(executor.map(sequential_merge_sort, chunks))
    
    # Merge chunks sequentially (like merge sort tree)
    while len(sorted_chunks) > 1:
        merged_chunks = []
        for i in range(0, len(sorted_chunks), 2):
            if i + 1 < len(sorted_chunks):
                merged_chunks.append(merge(sorted_chunks[i], sorted_chunks[i+1]))
            else:
                merged_chunks.append(sorted_chunks[i])
        sorted_chunks = merged_chunks
    
    return sorted_chunks[0]

# ====================== Benchmark ======================
def benchmark(dataset, max_workers):
    start = time.perf_counter()
    
    if max_workers == 1:
        result = sequential_merge_sort(dataset.copy())
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            result = parallel_merge_sort(dataset.copy(), executor, max_workers)
    
    runtime = time.perf_counter() - start
    return runtime, result

# ====================== Validation ======================
def validate(sorted_list):
    for i in range(len(sorted_list) - 1):
        if sorted_list[i].population > sorted_list[i + 1].population:
            return False
    return True

# ====================== Main ======================
def run_task5():
    print("6. Task 5 – Concurrent Programming\n")
    
    dataset = load_data("Data/world_cities_data.csv", limit=10000)
    print(f"Dataset loaded: {len(dataset)} cities\n")

    thread_counts = [1, 2, 4, 8]
    execution_times = []
    speedups = []
    sequential_time = None

    print("EXPERIMENTAL RESULTS")
    print("-" * 50)

    for threads in thread_counts:
        print(f"Running with {threads} thread{'s' if threads > 1 else ''}...", end=" ")
        runtime, sorted_data = benchmark(dataset, threads)
        execution_times.append(runtime)
        
        valid = validate(sorted_data)
        print(f"Done → {runtime:.4f} seconds | Valid: {valid}")
        
        if threads == 1:
            sequential_time = runtime
        speedups.append(sequential_time / runtime)

    print("\nSPEEDUP RESULTS")
    print("-" * 50)
    for t, s in zip(thread_counts, speedups):
        print(f"{t} Threads → {s:.2f}x Speedup")

    # ====================== Graphs ======================
    os.makedirs("Visualizations", exist_ok=True)
    
    plt.figure(figsize=(9, 6))
    plt.plot(thread_counts, execution_times, marker='o', linewidth=2.5, color='blue')
    plt.title("Execution Time vs Thread Count")
    plt.xlabel("Number of Threads")
    plt.ylabel("Execution Time (seconds)")
    plt.grid(True, alpha=0.3)
    plt.savefig("Visualizations/task5_execution_time.png", dpi=300, bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(9, 6))
    plt.plot(thread_counts, speedups, marker='o', linewidth=2.5, label="Measured Speedup", color='blue')
    plt.plot(thread_counts, thread_counts, linestyle='--', label="Ideal Speedup", color='orange')
    plt.title("Speedup vs Thread Count")
    plt.xlabel("Number of Threads")
    plt.ylabel("Speedup (x)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig("Visualizations/task5_speedup.png", dpi=300, bbox_inches='tight')
    plt.close()

    print("\n✅ Graphs saved in Visualizations folder!")


if __name__ == "__main__":
    run_task5()
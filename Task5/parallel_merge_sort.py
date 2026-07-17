import csv
import os
import time
import threading
import matplotlib.pyplot as plt

# City Class
class City:
    def __init__(self, name, population):
        self.name = name
        self.population = float(population) if population else 0

    def __repr__(self):
        return f"{self.name} ({self.population})"

# Load Dataset

def load_data(filepath, limit=None):
    cities = []

    with open(filepath, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        count = 0

        for row in reader:

            if limit and count >= limit:
                break

            try:
                cities.append(
                    City(
                        row["city"],
                        row["population"]
                    )
                )
                count += 1

            except ValueError:
                continue

    return cities

# Merge Function
merge_lock = threading.Lock()
def merge(left, right):
    # Critical Section protected by Mutex
    with merge_lock:

        merged = []

        i = 0
        j = 0

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
# Sequential Merge Sort
def sequential_merge_sort(arr):

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left = sequential_merge_sort(arr[:mid])
    right = sequential_merge_sort(arr[mid:])

    return merge(left, right)

# Thread Counter
class ThreadCounter:

    def __init__(self):

        self.count = 0
        self.lock = threading.Lock()

    def increment(self):

        with self.lock:
            self.count += 1

    def decrement(self):

        with self.lock:
            self.count -= 1
active_threads = ThreadCounter()
# Parallel Merge Sort
def parallel_merge_sort(arr, semaphore):

    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2

    left_half = arr[:mid]
    right_half = arr[mid:]

    left_sorted = []
    right_sorted = []

    # Try to create a new thread if a semaphore permit is available
    if semaphore.acquire(blocking=False):

        active_threads.increment()

        def sort_left():

            nonlocal left_sorted

            left_sorted = parallel_merge_sort(left_half, semaphore)

            active_threads.decrement()

            semaphore.release()

        thread = threading.Thread(target=sort_left)

        thread.start()

        # Main thread works on right half
        right_sorted = parallel_merge_sort(right_half, semaphore)

        # Wait until left thread finishes
        thread.join()

    else:

        # No thread available
        left_sorted = parallel_merge_sort(left_half, semaphore)
        right_sorted = parallel_merge_sort(right_half, semaphore)

    return merge(left_sorted, right_sorted)
# Benchmark Function
def benchmark(dataset, thread_count):

    # One thread means sequential implementation
    if thread_count == 1:

        start = time.perf_counter()

        result = sequential_merge_sort(dataset.copy())

        runtime = time.perf_counter() - start

        return runtime, result

    # Limit number of worker threads
    semaphore = threading.Semaphore(thread_count - 1)

    start = time.perf_counter()

    result = parallel_merge_sort(dataset.copy(), semaphore)

    runtime = time.perf_counter() - start

    return runtime, result

# Validation

def validate(sorted_list):

    for i in range(len(sorted_list) - 1):

        if sorted_list[i].population > sorted_list[i + 1].population:
            return False

    return True
    # Task 5 Runner

def run_task5():

    print("Task 5 : Concurrent Programming")

    dataset = load_data("Data\world_cities_data.csv", limit=10000)
    print(f"Loaded {len(dataset)} cities.")
    thread_counts = [1, 2, 4, 8]
    execution_times = []
    for threads in thread_counts:
        runtime, sorted_data = benchmark(dataset, threads)
        execution_times.append(runtime)
        print(
            f"Threads : {threads} | "
            f"Time : {runtime:.4f} sec | "
            f"Sorted : {validate(sorted_data)}"
        )
    # Speedup Calculation
    sequential_time = execution_times[0]
    speedups = []
    for t in execution_times:
        speedups.append(sequential_time / t)
    print("\nSpeedup Results")
    for threads, speed in zip(thread_counts, speedups):

        print(f"{threads} Threads -> {speed:.2f}x")
    os.makedirs("Visualizations", exist_ok=True)
    # Execution Time Graph
    plt.figure(figsize=(8, 6))
    plt.plot(
        thread_counts,
        execution_times,
        marker="o",
        linewidth=2
    )

    plt.title(
        "Execution Time vs Thread Count",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Number of Threads")
    plt.ylabel("Execution Time (seconds)")
    plt.grid(True)

    plt.savefig(
        "Visualizations/task5_execution_time.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    # Speedup Graph

    plt.figure(figsize=(8, 6))

    plt.plot(
        thread_counts,
        speedups,
        marker="o",
        linewidth=2,
        label="Measured Speedup"
    )

    plt.plot(
        thread_counts,
        thread_counts,
        linestyle="--",
        label="Ideal Speedup"
    )

    plt.title(
        "Speedup vs Thread Count",
        fontsize=16,
        fontweight="bold"
    )

    plt.xlabel("Number of Threads")
    plt.ylabel("Speedup (x)")
    plt.legend()
    plt.grid(True)

    plt.savefig(
        "Visualizations/task5_speedup.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("\nVisualizations Saved:")

# Main Function

if __name__ == "__main__":
    run_task5()
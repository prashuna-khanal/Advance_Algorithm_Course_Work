import csv
import time
import threading
import matplotlib.pyplot as plt

class City:
    def __init__(self, name, population):
        self.name = name
        self.population = float(population) if population else 0

    def __repr__(self):
        return f"{self.name}({self.population})"

def load_data(filepath, limit=None):
    cities = []
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        count = 0
        for row in reader:
            if limit and count >= limit: break
            try:
                cities.append(City(row['city'], row['population']))
                count += 1
            except ValueError:
                continue
    return cities

# ==========================================
# Task 5: Concurrent Parallel Merge Sort
# ==========================================

# A shared counter to demonstrate Mutex (Lock)
class ThreadSafeCounter:
    def __init__(self):
        self.value = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1

    def decrement(self):
        with self.lock:
            self.value -= 1
            
active_threads = ThreadSafeCounter()

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i].population <= right[j].population:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def parallel_merge_sort(arr, max_threads, semaphore):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # Try to acquire a permit to spawn a new thread for the left half
    # Using semaphore to limit active threads
    if semaphore.acquire(blocking=False):
        active_threads.increment()
        
        result_left = []
        def sort_left():
            nonlocal result_left
            result_left = parallel_merge_sort(left_half, max_threads, semaphore)
            active_threads.decrement()
            semaphore.release()
            
        t = threading.Thread(target=sort_left)
        t.start()
        
        # Current thread sorts the right half
        result_right = parallel_merge_sort(right_half, max_threads, semaphore)
        
        t.join() # Wait for left half to finish
        
    else:
        # If no threads are available, sort sequentially in the current thread
        result_left = parallel_merge_sort(left_half, max_threads, semaphore)
        result_right = parallel_merge_sort(right_half, max_threads, semaphore)

    return merge(result_left, result_right)


def run_task5():
    print("--- Task 5: Concurrent Programming ---")
    print("Loading Dataset...")
    dataset = load_data('Data/world_cities_data.csv', 10000) # 10,000 cities
    
    thread_counts = [1, 2, 4, 8]
    times = []
    
    print("\nStarting Threaded Benchmark...")
    for tc in thread_counts:
        # Create a semaphore with max permits = tc - 1 (since main thread counts as 1)
        sem = threading.Semaphore(tc - 1 if tc > 1 else 0)
        
        start_time = time.perf_counter()
        sorted_arr = parallel_merge_sort(dataset.copy(), tc, sem)
        end_time = time.perf_counter()
        
        duration = end_time - start_time
        times.append(duration)
        
        print(f"Threads: {tc} | Time taken: {duration:.4f} seconds")
        
        # Basic validation
        for i in range(len(sorted_arr)-1):
            assert sorted_arr[i].population <= sorted_arr[i+1].population

    # Calculate speedup relative to 1 thread
    base_time = times[0]
    speedups = [base_time / t for t in times]
    
    print("\n--- Analysis & Scalability ---")
    for tc, sp in zip(thread_counts, speedups):
        print(f"Threads: {tc} -> Speedup: {sp:.2f}x")
        
    print("\nExplanation of Overheads:")
    print("In Python (CPython), the Global Interpreter Lock (GIL) prevents true parallel execution")
    print("of Python bytecode across multiple CPU cores. As a result, CPU-bound tasks like Merge Sort")
    print("do not exhibit ideal linear speedup (e.g., 4 threads = 4x speedup).")
    print("Instead, we often observe a SLOWDOWN or flatline as thread count increases due to:")
    print(" 1. Thread creation overhead (cost of spawning OS threads).")
    print(" 2. Context switching overhead (threads fighting for the GIL).")
    print(" 3. Locking overhead (Mutex/Semaphore operations we used for synchronisation).")
    
    # Plotting
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 2, 1)
    plt.plot(thread_counts, times, marker='o', color='red')
    plt.title("Execution Time vs Thread Count")
    plt.xlabel("Thread Count")
    plt.ylabel("Time (seconds)")
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.plot(thread_counts, speedups, marker='o', color='blue')
    plt.plot(thread_counts, thread_counts, 'k--', alpha=0.5, label='Ideal Linear Speedup')
    plt.title("Speedup vs Thread Count")
    plt.xlabel("Thread Count")
    plt.ylabel("Speedup (x)")
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.savefig('Visualizations/task5_scalability.png')
    print("Scalability test complete. Results saved to Visualizations/task5_scalability.png")

if __name__ == "__main__":
    run_task5()

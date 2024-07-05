# thread_pool_example.py

from concurrent.futures import ThreadPoolExecutor

class ThreadPoolWorker:
    def __init__(self, num_threads):
        self.num_threads = num_threads

    def worker_function(self, value):
        # Simulate some work by returning the value squared
        return value ** 2

    def run_in_parallel(self, values):
        results = []
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            futures = {executor.submit(self.worker_function, val): val for val in values}
            for future in futures:
                result = future.result()
                results.append(result)
        return results

# Example usage (this can be removed or commented out during testing)
# if __name__ == '__main__':
#     worker = ThreadPoolWorker(4)
#     result = worker.run_in_parallel([1, 2, 3, 4])
#     print(result)

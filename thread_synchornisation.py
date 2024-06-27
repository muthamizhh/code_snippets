from concurrent.futures import ThreadPoolExecutor, as_completed
import os

def hello():
    l = [1, 2, 3, 4]
    return l

def sum_hello(index):
    l = hello()
    result_sum = sum(l)
    filename = f'sum_result_{index}.txt'

    # Write the sum to a text file
    with open(filename, 'w') as f:
        f.write(str(result_sum))

    return filename

def run_hello_in_parallel(num_threads):
    results = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = {executor.submit(sum_hello, i): i for i in range(num_threads)}

        for future in as_completed(futures):
            index = futures[future]
            try:
                result_filename = future.result()
                results.append(result_filename)
            except Exception as e:
                print(f"Exception occurred in thread {index}: {e}")

    return results

# Run the `sum_hello` function in parallel with 4 threads
parallel_results = run_hello_in_parallel(4)
print(parallel_results)

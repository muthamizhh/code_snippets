import splunklib.client as splunk_client
import splunklib.results as results
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import json
from datetime import datetime


class SplunkOperations:

    __slots__ = (
        'splunk_host',
        'splunk_port',
        'splunk_username',
        'splunk_password'
    )

    def __init__(self, splunk_host, splunk_port, splunk_username, splunk_password):
        self.splunk_host = splunk_host
        self.splunk_port = splunk_port
        self.splunk_username = splunk_username
        self.splunk_password = splunk_password

    def connect_to_splunk(self):
        try:
            service = splunk_client.connect(
                host=self.splunk_host,
                port=self.splunk_port,
                username=self.splunk_username,
                password=self.splunk_password
            )

            return service
        except ConnectionError as e:
            print('Error has occured in splunk connection', e)
            raise Exception from e

    def load_data_from_splunk(self, query, e_time, l_time):
        kwags_search = {"earliest_time": e_time, 'latest_time': l_time}
        service = self.connect_to_splunk()
        if service:
            jobs = service.jobs.create(query, **kwags_search)
            while not jobs.is_done():
                pass

            result = jobs.results()
            data = results.ResultsReader(result)
            l =[]
            for event in data:
                l.append(event)

        return l

    def sum_hello(self, index):
        l = self.load_data_from_splunk('search index=_internal | head 10', '-5m', 'now')
        result_sum = l
        print("lenght of the result is: ", result_sum)
        c = datetime.now()
        current_time = c.strftime('%H_%M_%S')
        if index == 0:

            filename = f"/Users/muthamizh/PycharmProjects/datapipeline/splunk_logs/splunk_data_{current_time}"
        else:
            filename = f"/Users/muthamizh/PycharmProjects/datapipeline/logs2/splunk_data_{current_time}"

        # Write the sum to a text file
        with open(filename, 'w') as f:
            json.dump(l, f)
        f.close()

        return filename

    def run_hello_in_parallel(self, num_threads):

        results = []

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            # futures = {executor.submit(self.sum_hello, i): i for i in range(num_threads)}
            futures = {}
            for i in range(num_threads):
                future = executor.submit(self.sum_hello, i)
                futures[future] = i

            for future in as_completed(futures):
                index = futures[future]
                try:

                    result_filename = future.result()
                    results.append(result_filename)
                except Exception as e:
                    print(f"Exception occurred in thread {index}: {e}")

        return results

# sb = SplunkOperations('localhost', 8089, 'Muthamizh', 'Rocky@001')
# # sb= SplunkOperations()
# print(sb.run_hello_in_parallel(2))

# Run the `sum_hello` function in parallel with 4 threads
# parallel_results = run_hello_in_parallel(4)
# print(parallel_results)

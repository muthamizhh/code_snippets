splunk_operaetino.py

import splunklib.client as splunk_client
import splunklib.results as splunk_results
import json

class SplunkOperations:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.service = None

    def connect(self):
        self.service = splunk_client.connect(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password
        )
        return self.service

    def extract_data_from_splunk(self, query):
        if self.service is None:
            self.connect()
        job = self.service.jobs.create(query)
        while not job.is_done():
            time.sleep(1)
        results = job.results()
        data = splunk_results.ResultsReader(results)
        return [event for event in data]

main_script.py

import os
from concurrent.futures import ThreadPoolExecutor
from splunk_operations import SplunkOperations
import json

def write_record_to_file(file_path, record):
    with open(file_path, 'w') as file:
        for event in record:
            json.dump(event, file)

def write_records_to_files(n):
    with ThreadPoolExecutor() as executor:
        sb = SplunkOperations(host='localhost', port=8089, password='password', username='username')
        futures = []
        for i in range(n):
            record = sb.extract_data_from_splunk("search index = _internal | head 10")
            print(record)
            if n == 0:
                directory = "/Users/muthamizh/PycharmProjects/datapipeline/splunk_logs"
            else:
                directory = "/Users/muthamizh/PycharmProjects/datapipeline/logs2"
            file_path = os.path.join(directory, f"file_{i}.json")
            futures.append(executor.submit(write_record_to_file, file_path, record))

        # Wait for all futures to complete
        for future in futures:
            print(future.result())

test_main_script.py


import unittest
from unittest.mock import patch, MagicMock
from main_script import write_records_to_files, write_record_to_file
from splunk_operations import SplunkOperations

class TestWriteRecordsToFiles(unittest.TestCase):

    @patch('main_script.SplunkOperations')
    @patch('main_script.write_record_to_file')
    def test_write_records_to_files(self, mock_write_record_to_file, mock_splunk_operations):
        # Mock the SplunkOperations instance and its method
        mock_sb_instance = MagicMock()
        mock_splunk_operations.return_value = mock_sb_instance
        mock_sb_instance.extract_data_from_splunk.return_value = [{"field1": "value1"}, {"field2": "value2"}]

        # Call the function to be tested
        write_records_to_files(2)

        # Check if the extract_data_from_splunk method was called twice
        self.assertEqual(mock_sb_instance.extract_data_from_splunk.call_count, 2)

        # Check if the write_record_to_file function was called twice with expected arguments
        expected_directory_0 = "/Users/muthamizh/PycharmProjects/datapipeline/splunk_logs"
        expected_directory_1 = "/Users/muthamizh/PycharmProjects/datapipeline/logs2"
        mock_write_record_to_file.assert_any_call(
            os.path.join(expected_directory_1, 'file_0.json'),
            [{"field1": "value1"}, {"field2": "value2"}]
        )
        mock_write_record_to_file.assert_any_call(
            os.path.join(expected_directory_1, 'file_1.json'),
            [{"field1": "value1"}, {"field2": "value2"}]
        )

if __name__ == '__main__':
    unittest.main()



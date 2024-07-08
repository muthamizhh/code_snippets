mongo_operation.py

from pymongo import MongoClient

class MongoDBOperations:
    def __init__(self, host, port, db_name, collection_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.collection = None

    def connect(self):
        self.client = MongoClient(self.host, self.port)
        db = self.client[self.db_name]
        self.collection = db[self.collection_name]

    def insert_records(self, records):
        if self.collection is None:
            self.connect()
        self.collection.insert_many(records)

main_script.py

import os
from concurrent.futures import ThreadPoolExecutor
from splunk_operations import SplunkOperations
from mongo_operations import MongoDBOperations
import json

def write_record_to_file(file_path, record):
    with open(file_path, 'w') as file:
        for event in record:
            json.dump(event, file)

def write_records_to_files_and_mongo(n):
    with ThreadPoolExecutor() as executor:
        sb = SplunkOperations(host='localhost', port=8089, password='password', username='username')
        mongo_ops = MongoDBOperations(host='localhost', port=27017, db_name='testdb', collection_name='testcollection')
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
            futures.append(executor.submit(mongo_ops.insert_records, record))

        # Wait for all futures to complete
        for future in futures:
            print(future.result())


test_main_script.py

import unittest
from unittest.mock import patch, MagicMock
from main_script import write_records_to_files_and_mongo, write_record_to_file
from splunk_operations import SplunkOperations
from mongo_operations import MongoDBOperations

class TestWriteRecordsToFilesAndMongo(unittest.TestCase):

    @patch('main_script.SplunkOperations')
    @patch('main_script.MongoDBOperations')
    @patch('main_script.write_record_to_file')
    def test_write_records_to_files_and_mongo(self, mock_write_record_to_file, mock_mongo_operations, mock_splunk_operations):
        # Mock the SplunkOperations instance and its method
        mock_sb_instance = MagicMock()
        mock_splunk_operations.return_value = mock_sb_instance
        mock_sb_instance.extract_data_from_splunk.return_value = [{"field1": "value1"}, {"field2": "value2"}]

        # Mock the MongoDBOperations instance and its method
        mock_mongo_instance = MagicMock()
        mock_mongo_operations.return_value = mock_mongo_instance

        # Call the function to be tested
        write_records_to_files_and_mongo(2)

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

        # Check if the insert_records method was called twice with expected arguments
        self.assertEqual(mock_mongo_instance.insert_records.call_count, 2)
        mock_mongo_instance.insert_records.assert_any_call([{"field1": "value1"}, {"field2": "value2"}])
        mock_mongo_instance.insert_records.assert_any_call([{"field1": "value1"}, {"field2": "value2"}])

if __name__ == '__main__':
    unittest.main()




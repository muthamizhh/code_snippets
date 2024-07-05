import unittest
from unittest.mock import patch, MagicMock
from extract_data_from_splunk import extract_data_from_splunk

class TestExtractDataFromSplunk(unittest.TestCase):

    @patch('splunklib.client.connect')
    @patch('splunklib.results.ResultsReader')
    def test_extract_data_from_splunk(self, mock_results_reader, mock_connect):
        # Mock Splunk connection
        mock_service = MagicMock()
        mock_connect.return_value = mock_service

        # Mock Splunk job and results
        mock_job = MagicMock()
        mock_service.jobs.create.return_value = mock_job
        mock_job.is_done.side_effect = [False, True]  # Simulate job completion after one check
        mock_job.results.return_value = [
            {"field1": "value1"},
            {"field2": "value2"}
        ]

        # Call the function to be tested
        data = extract_data_from_splunk('localhost', 8089, 'admin', 'password', 'search index=test')

        # Assertions
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["field1"], "value1")
        self.assertEqual(data[1]["field2"], "value2")

if __name__ == "__main__":
    unittest.main()


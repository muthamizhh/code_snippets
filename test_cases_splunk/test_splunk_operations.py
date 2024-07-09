import unittest
from unittest.mock import patch, MagicMock, mock_open
from testing.splunk_operations import SplunkOperations


class TestSplunkOperations(unittest.TestCase):

    @patch('testing.splunk_operations.splunk_client.connect')
    def test_connect_to_splunk(self, mock_connect):
        mock_service = MagicMock()
        mock_connect.return_value = mock_service

        splunk_ops = SplunkOperations('localhost', 8089, 'username', 'password')
        service = splunk_ops.connect_to_splunk()

        mock_connect.assert_called_once_with(
            host='localhost',
            port=8089,
            username='username',
            password='password'
        )
        self.assertEqual(service, mock_service)

    @patch.object(SplunkOperations, 'connect_to_splunk')
    def test_load_data_from_splunk(self, mock_connect_to_splunk):
        mock_service = MagicMock()
        mock_connect_to_splunk.return_value = mock_service

        mock_job = MagicMock()
        mock_service.jobs.create.return_value = mock_job
        mock_job.is_done.side_effect = [False, True]  # Simulate job completion after one check

        # Mocking the results to be an iterator
        mock_results = MagicMock()
        mock_results.__iter__.return_value = [
            {"field1": "value1"},
            {"field2": "value2"}
        ]
        mock_job.results.return_value = mock_results

        splunk_ops = SplunkOperations('localhost', 8089, 'username', 'password')
        data = splunk_ops.load_data_from_splunk('search index=test', '-5m', 'now')

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["field1"], "value1")
        self.assertEqual(data[1]["field2"], "value2")

    @patch.object(SplunkOperations, 'load_data_from_splunk')
    @patch('testing.splunk_operations.json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_sum_hello(self, mock_open, mock_json_dump, mock_load_data):
        mock_load_data.return_value = [
            {"field1": "value1"},
            {"field2": "value2"}
        ]

        splunk_ops = SplunkOperations('localhost', 8089, 'username', 'password')
        result_filename = splunk_ops.sum_hello(0)

        mock_load_data.assert_called_once_with('search index=_internal | head 10', '-5m', 'now')
        mock_open.assert_called_once()
        mock_json_dump.assert_called_once_with(mock_load_data.return_value, mock_open())

        self.assertIn("splunk_logs/splunk_data_", result_filename)

    @patch.object(SplunkOperations, 'sum_hello')
    def test_run_hello_in_parallel(self, mock_sum_hello):
        mock_sum_hello.side_effect = lambda i: f"file_{i}.json"

        splunk_ops = SplunkOperations('localhost', 8089, 'username', 'password')
        results = splunk_ops.run_hello_in_parallel(2)

        self.assertEqual(results, ["file_0.json", "file_1.json"])
        self.assertEqual(mock_sum_hello.call_count, 2)
        mock_sum_hello.assert_any_call(0)
        mock_sum_hello.assert_any_call(1)


if __name__ == "__main__":
    unittest.main()

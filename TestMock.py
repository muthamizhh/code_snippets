# test_thread_pool_example.py

import pytest
from unittest.mock import patch, MagicMock
from thread_pool_example import ThreadPoolWorker

@patch('thread_pool_example.ThreadPoolExecutor')
def test_run_in_parallel(mock_executor):
    # Mock the ThreadPoolExecutor instance and methods
    mock_executor_instance = MagicMock()
    mock_executor.return_value = mock_executor_instance

    # Create a mock future object
    mock_future = MagicMock()
    mock_future.result.side_effect = [1, 4, 9, 16]  # Return values for futures

    # Set the map method to return a list of mock futures
    mock_executor_instance.submit.side_effect = [mock_future] * 4

    # Create an instance of ThreadPoolWorker with test parameters
    worker = ThreadPoolWorker(4)
    
    # Call the method to be tested
    result = worker.run_in_parallel([1, 2, 3, 4])

    # Assertions to ensure the function behaves as expected
    mock_executor.assert_called_once_with(max_workers=4)
    assert result == [1, 4, 9, 16]
    assert mock_executor_instance.submit.call_count == 4

# To run the tests, use the command: pytest test_thread_pool_example.py

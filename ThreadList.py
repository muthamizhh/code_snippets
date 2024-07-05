import unittest
from unittest.mock import patch, MagicMock
import os

# Function to be tested
def write_record_to_file(file_path, record):
    with open(file_path, 'w') as file:
        file.write(record + '\n')

# Function using ThreadPoolExecutor
def write_records_to_files(records, directory):
    with ThreadPoolExecutor() as executor:
        futures = []
        for i, record in enumerate(records):
            file_path = os.path.join(directory, f"file_{i}.txt")
            futures.append(executor.submit(write_record_to_file, file_path, record))

        # Wait for all futures to complete
        for future in futures:
            future.result()

# Test case using unittest and unittest.mock
class TestWriteRecords(unittest.TestCase):

    @patch('builtins.open', create=True)
    @patch('concurrent.futures.ThreadPoolExecutor')
    def test_write_records_to_files(self, mock_executor, mock_open):
        # Mock ThreadPoolExecutor
        mock_executor_instance = MagicMock()
        mock_executor.return_value.__enter__.return_value = mock_executor_instance

        # Mock submit method to simulate writing records
        def mock_submit(func, file_path, record):
            func(file_path, record)
            return MagicMock()

        mock_executor_instance.submit.side_effect = mock_submit

        # Arrange
        records = ["record1", "record2", "record3"]
        directory = "/path/to/test_dir"  # Replace with your test directory path

        # Act
        write_records_to_files(records, directory)

        # Assert
        for i, record in enumerate(records):
            file_path = os.path.join(directory, f"file_{i}.txt")
            with open(file_path, 'r') as f:
                lines = f.readlines()
                self.assertEqual(lines, [record + '\n'])

if __name__ == "__main__":
    unittest.main()

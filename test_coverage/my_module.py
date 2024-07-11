pytest test_my_module.py --cov=my_module --cov-report=html -v

def write_to_file(data, path):
    with open(path, 'w') as file:
        file.write(data)

def sample():
    data = "Sample data"
    path = "sample_path.txt"
    write_to_file(data, path)


test_my_module.py

import unittest
from unittest.mock import patch
from my_module import sample

class TestSampleFunction(unittest.TestCase):

    @patch('my_module.write_to_file')
    def test_sample(self, mock_write_to_file):
        sample()
        mock_write_to_file.assert_called_once_with("Sample data", "sample_path.txt")

if __name__ == "__main__":
    unittest.main()

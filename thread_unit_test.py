import pytest
from concurrent.futures import ThreadPoolExecutor
import os

def write_record_to_file(file_path, record):
    with open(file_path, 'w') as file:
        file.write(record + '\n')

def write_records_to_files(records, directory):
    with ThreadPoolExecutor() as executor:
        futures = []
        for i, record in enumerate(records):
            file_path = os.path.join(directory, f"file_{i}.txt")
            futures.append(executor.submit(write_record_to_file, file_path, record))

        # Wait for all futures to complete
        for future in futures:
            future.result()

def test_threaded_write_records_to_files(tmpdir):
    # Arrange
    records = ["record1", "record2", "record3"]
    directory = tmpdir.mkdir("test_dir")

    # Act
    write_records_to_files(records, str(directory))

    # Assert
    for i, record in enumerate(records):
        file_path = directory.join(f"file_{i}.txt")
        with open(file_path, 'r') as f:
            lines = f.readlines()
            assert lines == [record + '\n']

if __name__ == "__main__":
    pytest.main([__file__])

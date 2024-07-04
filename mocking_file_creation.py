import pytest
import json

def write_records_to_file(file_path, records):
    with open(file_path, 'w') as file:

        json.dump(records, file)


def test_write_records_to_file(tmpdir):
    # Arrange
    records = [{'name': 'hello','tour': 'India'},{'age': 23}]
    file = tmpdir.join("test_file.json")


    # Act
    write_records_to_file(file, records)

    # Assert
    with open(file, 'r') as f:
        lines = json.load(f)
        print(lines)
        assert lines == [{'name': 'hello','tour': 'India'},{'age': 23}]

#
# if __name__ == "__main__":
#     pytest.main([__file__])

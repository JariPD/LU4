import pytest
from data_manager import *

@pytest.fixture
def temp_json_file(tmp_path):
    """
    A pytest fixture to create a temporary JSON file.
    """
    file_path = tmp_path / "credentials.json"
    yield str(file_path)  # Provide the path to the test function
    # Cleanup is handled automatically by `tmp_path`

def test_initialize_jsons_file(temp_json_file):
    """
    Test that the initialize_credentials_file function creates an empty JSON file.
    """
    # Ensure the file doesn't exist initially
    assert not os.path.exists(temp_json_file)

    # Initialize the file
    initialize_json_file(temp_json_file)

    # Check the file now exists and contains an empty JSON object
    assert os.path.exists(temp_json_file)
    with open(temp_json_file, "r") as f:
        data = json.load(f)
    assert data == {}

def test_save_json(temp_json_file):
    """
    Test that save_credentials writes data correctly to the file.
    """
    credentials = {"user": "testuser", "password": "testpass", "role": "testrole"}

    # Save credentials
    save_json(credentials, temp_json_file)

    # Verify the data was written correctly
    with open(temp_json_file, "r") as f:
        data = json.load(f)
    assert data == credentials

def test_load_json(temp_json_file):
    """
    Test that load_credentials reads data correctly from the file.
    """
    # Prepare test data
    credentials = {"user": "testuser", "password": "testpass"}
    with open(temp_json_file, "w") as f:
        json.dump(credentials, f)

    # Load credentials
    loaded_credentials = load_json(temp_json_file)

    # Verify the loaded data matches the saved data
    assert loaded_credentials == credentials

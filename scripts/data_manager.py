import json
import os

# Initialize the JSON file if it doesn't exist
def initialize_credentials_file(file):
    if not os.path.exists(file):
        with open(file, "w") as file:
            json.dump({}, file)  # Create an empty JSON object

# Load credentials from the JSON file
def load_credentials(file):
    with open(file, "r") as file:
        return json.load(file)

# Save credentials to the JSON file
def save_credentials(credentials, file):
    with open(file, "w") as file:
        json.dump(credentials, file, indent=4)
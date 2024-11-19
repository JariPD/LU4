import json
import os

# Initialize the JSON file if it doesn't exist
def initialize_json_file(file):
    if not os.path.exists(file):
        with open(file, "w") as file:
            json.dump({}, file)  # Create an empty JSON object

# Load from JSON file
def load_json(file):
    with open(file, "r") as file:
        return json.load(file)

# Save to JSON file
def save_json(dictionary, file):
    with open(file, "w") as file:
        json.dump(dictionary, file, indent=4)
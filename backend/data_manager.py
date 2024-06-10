import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, db

# Load environment variables from .env file
load_dotenv()

# Get the path to the Firebase service account key JSON file from the environment variable
firebase_credentials_path = os.getenv('FIREBASE_CREDENTIALS')

# Initialize Firebase
cred = credentials.Certificate(firebase_credentials_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cuesty-424dc-default-rtdb.firebaseio.com/'
})


# Function to save server mapping data to Firebase
def save_server_mapping_data(server_id, data):
    ref = db.reference(f'Servers/{server_id}')

    # Use a transaction to update the data atomically
    def update_server_mapping(current_data):
        # If the current data is None, set the new data
        if current_data is None:
            return data
        # Otherwise, update the current data with the new data
        current_data.update(data)
        return current_data

    # Commit the transaction
    db.reference(f'Servers/{server_id}').transaction(update_server_mapping)
    print(f"Server mapping saved to Firebase under server_id: {server_id}")

# Function to load server mapping data from Firebase
def load_server_mapping(server_id):
    ref = db.reference(f'Servers/{server_id}')
    return ref.get() or {}


def variable_finder(server_id, variable_name):
    ref = db.reference(f'Servers/{server_id}/variables/{variable_name}')
    variable_id = ref.get()
    if variable_id:
        return int(variable_id)
    else:
        raise ValueError(f"Variable '{variable_name}' not found for guild ID {server_id}.")

# Function to load user data from Firebase
def load_data(user_id):
    ref = db.reference(f'users/{user_id}')
    return ref.get() or {}

# Function to save user data to Firebase
def save_data(data):
    if 'User_Main' not in data or 'user_id' not in data['User_Main']:
        raise KeyError("The user data does not contain a 'User_Main' key or 'user_id' key within 'User_Main'.")

    user_id = data['User_Main']['user_id']
    ref = db.reference(f'users/{user_id}')
    ref.set(data)

# Function to load quest data from Firebase
def load_quest_data(quest_id):
    ref = db.reference(f'quests/{quest_id}')
    return ref.get() or {}

# Function to save quest data to Firebase
def save_quest_data(data):
    if 'Quest_Main' not in data or 'quest_id' not in data['Quest_Main']:
        raise KeyError("The quest data does not contain a 'Quest_Main' key or 'quest_id' key within 'Quest_Main'.")

    quest_id = data['Quest_Main']['quest_id']
    ref = db.reference(f'quests/{quest_id}')
    ref.set(data)

from firebase_admin import db


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

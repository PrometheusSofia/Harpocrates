import json
import string
import secrets
import os


DATA_PATH = "data/passwords.json"

def load_passwords():
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)

    try:
        with open(DATA_PATH, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is corrupted, create an empty JSON file
        with open(DATA_PATH, "w") as file:
            json.dump([], file, indent=4)  
        return []


def save_password(password_data):
    passwords = load_passwords()
    passwords.append(password_data)
    with open("data/passwords.json", "w") as file:
        json.dump(passwords, file)

def generate_password(length: int) -> str:
    print("Generating password")
    if length < 4:
        raise ValueError("Password length must be at least 4 for complexity.")

    # Character pools
    uppercase = string.ascii_uppercase
    lowercase = string.ascii_lowercase
    digits = string.digits
    symbols = string.punctuation

    # Ensure password contains at least one of each type
    password = [
        secrets.choice(uppercase),
        secrets.choice(lowercase),
        secrets.choice(digits),
        secrets.choice(symbols)
    ]

    # Fill the rest of the password length randomly
    all_characters = uppercase + lowercase + digits + symbols
    password += [secrets.choice(all_characters) for _ in range(length - 4)]

    # Shuffle to randomize character order
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)

def check_password_strength(password):
    password = str(password)  
    SPECIAL_CHARACTERS = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/\\`~"

    characteristics = {
        "lowercase": any(char.islower() for char in password),
        "uppercase": any(char.isupper() for char in password),
        "numbers": any(char.isdigit() for char in password),
        "special": any(char in SPECIAL_CHARACTERS for char in password)
    }
    print(characteristics)
    return characteristics

def delete_password(source, username):
    passwords = load_passwords()
    
    # Find the entry to delete
    updated_passwords = [entry for entry in passwords if not (entry["Source"] == source and entry["Username"] == username)]

    if len(updated_passwords) == len(passwords):
        return False 

    # Save the updated list back to the file
    with open("data/passwords.json", "w") as file:
        json.dump(updated_passwords, file)

    return True  

import json

def login(email, password):
    accounts = get_accounts()
    for account in accounts:
        if account["email"] == email and account["password"] == password:
            return True
    return False

def get_accounts():
    try:
        with open("data/accounts.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

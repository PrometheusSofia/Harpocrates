import json

def load_settings():
    try:
        with open("data/settings.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"theme": "Light"}

def save_settings(settings):
    with open("data/settings.json", "w") as file:
        json.dump(settings, file)

def toggle_theme(current_theme):
    return "Dark" if current_theme == "Light" else "Light"

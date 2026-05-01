import json
import os


SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "blue",
    "difficulty": "normal"
}


def load_settings():
    # Load settings from settings.json
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
        settings = json.load(file)

    # Add missing default keys
    for key, value in DEFAULT_SETTINGS.items():
        if key not in settings:
            settings[key] = value

    return settings


def save_settings(settings):
    # Save settings to settings.json
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(settings, file, indent=4)


def load_leaderboard():
    # Load leaderboard from leaderboard.json
    if not os.path.exists(LEADERBOARD_FILE):
        save_leaderboard([])
        return []

    with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_leaderboard(data):
    # Save leaderboard to leaderboard.json
    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def add_score(name, score, distance, coins):
    # Add new result and keep top 10
    data = load_leaderboard()

    data.append({
        "name": name,
        "score": score,
        "distance": distance,
        "coins": coins
    })

    data.sort(key=lambda x: (x["score"], x["distance"]), reverse=True)
    data = data[:10]

    save_leaderboard(data)


def get_top10():
    # Return top 10 scores
    return load_leaderboard()[:10]
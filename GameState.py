import json
from Player import Player

SAVE_FILE = "gamestate.json"


def update_game(player1, player2):
    data = [player1.to_dict(), player2.to_dict()]  # build first so an error keeps the old save
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except OSError as error:
        print(f"Could not save game: {error}")


def clear_game():
    with open(SAVE_FILE, "w") as f:
        json.dump([], f)


def resume_game():
    try:
        with open(SAVE_FILE, "r") as f:
            text = f.read()
        if not text.strip():
            return None  # empty file, no save yet
        contents = json.loads(text)
        if len(contents) != 2:
            return None
        return [Player.from_dict(d) for d in contents]
    except FileNotFoundError:
        return None
    except (json.JSONDecodeError, KeyError, TypeError, IndexError):
        print("Last game save is corrupt")
        return None
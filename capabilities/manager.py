import json

from paths import CAPABILITIES_DIR

CAPABILITIES_FILE = CAPABILITIES_DIR / "capabilities.json"


def load_capabilities():

    with open(CAPABILITIES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_capabilities(data):

    with open(CAPABILITIES_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def is_enabled(name):

    data = load_capabilities()

    return data.get(name, {}).get("enabled", False)


def set_enabled(name, value):

    data = load_capabilities()

    if name in data:

        data[name]["enabled"] = value

        save_capabilities(data)

def load_json(path):

    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(path, data):

    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
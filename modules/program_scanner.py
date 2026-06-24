import os
import json
from paths import PROGRAMS_FILE
from theme import *

from paths import SCAN_SETTINGS_FILE
def load_scan_folders():

    with open(SCAN_SETTINGS_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    folders = []

    for folder in data["folders"]:

        if folder["enabled"]:

            folders.append(folder["path"])

    return folders
folders=load_scan_folders()
def scan_programs():

    programs = {}

    for folder in folders:

        if not os.path.exists(folder):
            continue

        for root, dirs, files in os.walk(folder):

            for file in files:

                if file.lower().endswith(".exe"):

                    name = os.path.splitext(file)[0]

                    programs[name] = os.path.join(root, file)

    return programs
def save_programs(programs):

    data = {}

    for name, path in programs.items():

        data[name] = {
            "path": path
        }

    with open(PROGRAMS_FILE, "w", encoding="utf-8") as file:

        json.dump(data, file, ensure_ascii=False, indent=4)
        print(f'{SYSTEM}данные успешно сохранены{RESET}')

def update_program_database():

    programs = scan_programs()

    save_programs(programs)

    return len(programs)


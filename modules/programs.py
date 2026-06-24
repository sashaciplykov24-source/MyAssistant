import subprocess
import json

from paths import CAPABILITIES_DIR

PROGRAMS_FILE = CAPABILITIES_DIR / "programs.json"


def load_programs():

    with open(PROGRAMS_FILE, encoding="utf-8") as file:
        return json.load(file)


def open_program(name):

    programs = load_programs()

    if name not in programs:
        return False

    path = programs[name]["path"]

    subprocess.Popen(path)

    return True
import subprocess
import json
import os

from paths import ALIASES_FILE, PROGRAMS_FILE


def normalize_name(name):

    if not name:
        return ""

    return name.strip().lower()


def load_programs():

    with open(PROGRAMS_FILE, encoding="utf-8") as file:
        return json.load(file)


def load_aliases():

    if not ALIASES_FILE.exists():
        return {}

    with open(ALIASES_FILE, encoding="utf-8") as file:
        return json.load(file)


def find_program(name):

    programs = load_programs()
    aliases = load_aliases()
    requested_name = normalize_name(name)

    if name in programs:
        return programs[name]

    for program_name, program_data in programs.items():

        if normalize_name(program_name) == requested_name:
            return program_data

    for program_name, alias_list in aliases.items():

        normalized_aliases = [
            normalize_name(alias)
            for alias in alias_list
        ]

        if requested_name == normalize_name(program_name) or requested_name in normalized_aliases:

            if program_name in programs:
                return programs[program_name]

            for scanned_program_name, program_data in programs.items():

                if normalize_name(scanned_program_name) == normalize_name(program_name):
                    return program_data

    return None


def open_program(name):

    program = find_program(name)

    if not program:
        return False

    path = program.get("path")

    if not path:
        return False

    if not os.path.exists(path):
        return False

    try:
        subprocess.Popen(path)
    except OSError:
        return False

    return True

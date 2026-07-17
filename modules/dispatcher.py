from modules.programs import open_program
import os
from theme import *

COMMAND_PREFIXES = {
    "OPEN_PROGRAM": ("open_program", "program"),
    "CREATE_FOLDER": ("create_folder", "path"),
    "DELETE_FILE": ("delete_file", "path"),
}


def parse_command(answer):

    lines = answer.strip().splitlines()

    if not lines:
        return None

    first_line = lines[0].strip()

    if ":" not in first_line:
        return None

    command_name, value = first_line.split(":", 1)
    command_name = command_name.strip().upper()
    value = value.strip()

    if command_name not in COMMAND_PREFIXES:
        return None

    if not value:
        return None

    action, argument_name = COMMAND_PREFIXES[command_name]

    return {
        "command": action,
        argument_name: value
    }


def dispatch(command):

    action = command.get("command")

    if action == "open_program":
        program = command.get("program")

        if not program:
            return "Не указана программа."

        if open_program(program):
            return "Программа запущена."

        return "Не удалось открыть программу."

    if action == "create_folder":

        path = command.get("path")

        if not path:
            return "Не указан путь к папке."

        try:
            os.makedirs(path, exist_ok=True)
        except OSError:
            return "Не удалось создать папку."

        return "Папка создана."

    elif action == "delete_file":

        path = command.get("path")

        if not path:
            return "Не указан путь к файлу."

        if os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                return "Не удалось удалить файл."

            return "Файл удалён."

        return "Файл не найден."

    else:

        return f"{ERROR}Неизвестная команда.{RESET}"

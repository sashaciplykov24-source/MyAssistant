from modules.programs import open_program
import os
import json
from paths import FOLDER_SETTINGS_FILE
from theme import *

COMMAND_PREFIXES = {
    "OPEN_PROGRAM": ("open_program", "program"),
    "OPEN_FOLDER": ("open_folder", "path"),
    "LIST_FOLDER": ("list_folder", "path"),
    "PATH_INFO": ("path_info", "path"),
    "CREATE_FOLDER": ("create_folder", "path"),
    "CREATE_FILE": ("create_file", "path"),
    "DELETE_FILE": ("delete_file", "path"),
    "DELETE_EMPTY_FOLDER": ("delete_empty_folder", "path"),
}

DEFAULT_FOLDER_LIST_LIMIT = 50


def format_size(size):

    for unit in ["Б", "КБ", "МБ", "ГБ", "ТБ"]:

        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} ПБ"


def load_folder_list_limit():

    if not FOLDER_SETTINGS_FILE.exists():
        return DEFAULT_FOLDER_LIST_LIMIT

    try:
        with open(FOLDER_SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)
    except (OSError, json.JSONDecodeError):
        return DEFAULT_FOLDER_LIST_LIMIT

    limit = settings.get("list_limit")

    if not isinstance(limit, int) or limit < 1:
        return DEFAULT_FOLDER_LIST_LIMIT

    return limit


def parse_command(answer):

    lines = [
        line.strip()
        for line in answer.strip().splitlines()
        if line.strip()
    ]

    if not lines:
        return None

    first_line = lines[0].strip("`").strip()

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

    if action == "open_folder":

        path = command.get("path")

        if not path:
            return "Не указан путь к папке."

        if not os.path.exists(path):
            return "Папка не найдена."

        if not os.path.isdir(path):
            return "Это не папка."

        try:
            os.startfile(path)
        except OSError:
            return "Не удалось открыть папку."

        return "Папка открыта."

    elif action == "list_folder":

        path = command.get("path")

        if not path:
            return "Не указан путь к папке."

        if not os.path.exists(path):
            return "Папка не найдена."

        if not os.path.isdir(path):
            return "Это не папка."

        try:
            items = sorted(os.listdir(path))
        except OSError:
            return "Не удалось прочитать папку."

        if not items:
            return "Папка пустая."

        result = []

        list_limit = load_folder_list_limit()

        for item in items[:list_limit]:
            item_path = os.path.join(path, item)

            if os.path.isdir(item_path):
                result.append(f"[Папка] {item}")
            else:
                result.append(f"[Файл] {item}")

        if len(items) > list_limit:
            result.append(f"...и ещё {len(items) - list_limit}")

        return "\n".join(result)

    elif action == "path_info":

        path = command.get("path")

        if not path:
            return "Не указан путь."

        if not os.path.exists(path):
            return "Путь не найден."

        if os.path.isdir(path):
            try:
                items_count = len(os.listdir(path))
            except OSError:
                return "Это папка. Не удалось прочитать содержимое."

            return f"Это папка. Элементов внутри: {items_count}."

        if os.path.isfile(path):
            try:
                size = os.path.getsize(path)
            except OSError:
                return "Это файл. Не удалось узнать размер."

            return f"Это файл. Размер: {format_size(size)}."

        return "Путь существует, но это не обычный файл и не папка."

    elif action == "create_folder":

        path = command.get("path")

        if not path:
            return "Не указан путь к папке."

        try:
            os.makedirs(path, exist_ok=True)
        except OSError:
            return "Не удалось создать папку."

        return "Папка создана."

    elif action == "create_file":

        path = command.get("path")

        if not path:
            return "Не указан путь к файлу."

        if os.path.exists(path):
            return "Файл уже существует."

        try:
            open(path, "x", encoding="utf-8").close()
        except OSError:
            return "Не удалось создать файл."

        return "Файл создан."

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

    elif action == "delete_empty_folder":

        path = command.get("path")

        if not path:
            return "Не указан путь к папке."

        if not os.path.exists(path):
            return "Папка не найдена."

        if not os.path.isdir(path):
            return "Это не папка."

        try:
            os.rmdir(path)
        except OSError:
            return "Папка не пустая или её не удалось удалить."

        return "Пустая папка удалена."

    else:

        return f"{ERROR}Неизвестная команда.{RESET}"

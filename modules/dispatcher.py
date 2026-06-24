import json
from modules.programs import open_program
import subprocess
import os
from theme import *

def dispatch(command):

    action = command.get("command")

    if action == "open_program":
        program = command.get("program")
        if open_program(program):
            return "Программа запущена."

        return "Не удалось открыть программу."

    if action == "create_folder":

        path = command.get("path")

        os.makedirs(path, exist_ok=True)

        return "Папка создана."

    elif action == "delete_file":

        path = command.get("path")

        if os.path.exists(path):
            os.remove(path)
            return "Файл удалён."

        return "Файл не найден."

    else:

        return f"{ERROR}Неизвестная команда.{RESET}"
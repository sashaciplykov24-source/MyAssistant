import os

def open_file(path):

    if not os.path.exists(path):
        return "Файл не найден."

    os.startfile(path)

    return "Файл открыт."
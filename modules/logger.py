from datetime import datetime

LOG_FILE = "data/logs.txt"

def write_system(message):

    now = datetime.now()

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        file.write("=" * 50 + "\n")
        file.write(now.strftime("[%d.%m.%Y %H:%M:%S]\n\n"))

        file.write("[СИСТЕМА]\n")
        file.write(message + "\n\n")

def write_log(user_message, assistant_message):

    now = datetime.now()

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        file.write("=" * 50 + "\n")
        file.write(now.strftime("[%d.%m.%Y %H:%M:%S]\n\n"))

        file.write("Ты:\n")
        file.write(user_message + "\n\n")

        file.write("ИИ:\n")
        file.write(assistant_message + "\n\n")
from modules.ai import ask_ai

from settings.config import VERSION_PROGRAM

from paths import *

from theme import *

from modules.logger import write_log

from modules.logger import write_system

from modules.memory import load_history, save_history

import os

import json

from paths import SCAN_SETTINGS_FILE

def load_settings():

    with open(SCAN_SETTINGS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
def save_settings(data):

    with open(SCAN_SETTINGS_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
def add_folder(name, path):

    data = load_settings()

    data["folders"].append({
        "name": name,
        "path": path,
        "enabled": True
    })

    save_settings(data)
def remove_folder(name):

    data = load_settings()

    data["folders"] = [
        folder for folder in data["folders"]
        if folder["name"] != name
    ]

    save_settings(data)
def set_enabled(name, enabled):

    data = load_settings()

    for folder in data["folders"]:

        if folder["name"] == name:

            folder["enabled"] = enabled

            break

    save_settings(data)
def save_model(model):

    with open("settings/model.json", "w", encoding="utf-8") as file:

        json.dump(
            {"model": model},
            file,
            ensure_ascii=False,
            indent=4
        )
import ollama

def model_exists(model_name):

    models = ollama.list()

    for model in models.models:
        if model.model == model_name:
            return True

    return False

def get_models():

    models = ollama.list()

    result = []

    for model in models.models:
        result.append(model.model)

    return result
def show_info(history):

    print("\n========================")
    print(" MyAssistant ")
    print("========================")

    print(f"Версия: {VERSION_PROGRAM}")

    try:
        with open(MODEL_FILE, "r", encoding="utf-8") as file:
            model_data = json.load(file)
            print(f"Модель: {model_data['model']}")
    except:
        print("Модель: неизвестно")

    print(f"Сообщений в памяти: {len(history)}")

    try:
        with open(PROGRAMS_FILE, "r", encoding="utf-8") as file:
            programs = json.load(file)

        print(f"Найдено программ: {len(programs)}")

    except:
        print("Найдено программ: 0")

    print("========================")


from modules.program_scanner import update_program_database
#
#count = update_program_database()

#print(f"Найдено {count} программ.")
#
def format_size(size):

    for unit in ["Б","КБ","МБ","ГБ","ТБ"]:

        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024
    return f"{size:.2f} ПБ"

def clear_history():
    with open("data/history.json", "w", encoding="utf-8") as file:
        json.dump([], file, ensure_ascii=False, indent=4)

def clear_logs():
    with open("data/logs.txt", "w", encoding="utf-8") as file:
        file.write("")

history = load_history()

print(f'{SYSTEM}для открытия меню настроек введите "/setting{RESET}"')
print(f'{SYSTEM}для выхода "/exit{RESET}"')
print(f'{SYSTEM}для помощи введите "/help"{RESET}')
print("================================")
print(f" {SYSTEM}Локальный помощник запущен{RESET} ")
write_system("Помощник запущен")
print("================================")

while True:

    size_logs = os.path.getsize(LOG_FILE)
    size_history = os.path.getsize(HISTORY_FILE)
    if format_size(size_history).split()[1]=='ГБ':
        if float(format_size(size_history)).split()[0]>=10:
            print(f'{ERROR}внимание память слишком большая{RESET}')
    if format_size(size_logs).split()[1]=='ГБ':
        if float(format_size(size_logs)).split()[0]>=5:
            print(f'{ERROR}внимание логи слишком большие{RESET}')

    user = input("\nТы: ")

    if user.lower() == "/exit":
        break
    elif user.lower()=='/setting':
        size_history = os.path.getsize(HISTORY_FILE)
        size_logs = os.path.getsize(LOG_FILE)
        print("================================")
        print(f'размер логов= {format_size(size_logs)}')
        print(f'размер памяти= {format_size(size_history)}')
        while True:
            print('1-сбросить память,2-выйти,3-сбросить логи,4-открыть логи,5-открыть память')
            q=input('>')
            if q=='1':
                clear_history()
                history.clear()
                print('память очищена')
                write_system(f"память очищена")
            elif q=='2':
                break
            elif q=='3':
                clear_logs()
                print('логи очищены')
                write_system(f"логи очищены")
            elif q=='4':
                os.startfile(LOG_FILE)
                write_system(f'открыты логи')
            elif q=='5':
                os.startfile(HISTORY_FILE)
                write_system(f'открыта память')
            else:
                print(F'{ERROR}команда не распозднана{RESET}')
                write_system("ошибка команды в настройках")
        continue
    elif user.lower() == "/help":
        print("================================")
        print('"/setting"-меню настроек')
        print('"/help"-меню помощи')
        print('"/scan setting"-настройка сканирования программм')
        print('"/scan"-запуск сканирования программм')
        print('"/models"-смена AI модели')
        print("================================")
        continue
    elif user.lower() == "/scan setting":
        while True:
            print("================================")
            fol_name = []
            fol_enabled=[]
            id_fol=dict()
            active='enabled'
            with open(SCAN_SETTINGS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            for folder in data["folders"]:
                fol_name.append(folder["name"])
                fol_enabled.append(folder["enabled"])
            for i in range(len(fol_name)):
                if fol_enabled[i]==True:
                    active='активно'
                else:
                    active='неактивно'
                id_fol[i]=fol_name[i]
                print(i,fol_name[i],active)
            print('1-добавить папку,2-выйти,3-удалить папку,4-изменить активность')
            q=input('>')
            if q=='1':
                print('напишите название папки')
                fold=input('>')
                print("напишите путь к папке в формате (C:\\\\Program Files (x86)\\\\Steam)")
                way=input('>')
                add_folder(fold,way)
                write_system(f'добавлена папка {fold} в сканирование')
            elif q=='2':
                break
            elif q=='3':
                print('напишите номер папки')
                n=int(input('>'))
                if n>=len(id_fol) or n<0:
                    print('такого номера нет')
                else:
                    remove_folder(fol_name[n])
                    write_system(f'удалена папка {fol_name[n]} из сканирования')
            elif q=='4':
                activein=False
                print('напишите номер папки')
                n=int(input('>'))
                if n>=len(id_fol) or n<0:
                    print('такого номера нет')
                else:
                    if fol_enabled[n]==True:
                        activein=False
                    else:
                        activein=True
                    set_enabled(fol_name[n],activein)
                    write_system(f'активность папки {fol_name[n]} изменено на {activein}')
            else:
                print(F'{ERROR}команда не распозднана{RESET}')
                write_system("ошибка команды в настройках сканирования")
        continue
    elif user.lower() == "/scan":
        print("================================")
        write_system('сканирование запущенно')
        count = update_program_database()
        print(f"Найдено {count} программ.")
        write_system(f'сканирование завершено. Найдено {count} программ. они добавлены в programs')
        print("================================")
        continue
    elif user.lower() == "/models":
        print("================================")
        models = get_models()
        print("Доступные модели:")
        for i, model in enumerate(models, start=1):
            print(f"{i}. {model}")
        print('введите название своей локальной AI модели')
        mod=input('>')
        if model_exists(mod):
            save_model(mod)
            print(f'{SYSTEM}модель успешно изменена на- "{mod}" {RESET}')
            write_system(f'пользователь установил модель AI агента-"{mod}"')
        else:
            print(f'{ERROR}модель не найдена{RESET}')
            write_system(f'модель-"{mod}" не найдена')
        continue
    elif user.lower() == "/info":
        show_info(history)
        continue

    history.append({
        "role": "user",
        "content": user
    })

    answer = ask_ai(history)

    history.append({
        "role": "assistant",
        "content": answer
    })

    save_history(history)

    write_log(user, answer)

    print(f"\n{AI}ИИ:{RESET} {answer}")
from pathlib import Path

# Папка, в которой находится проект
PROJECT_DIR = Path(__file__).resolve().parent

# Основные папки
DATA_DIR = PROJECT_DIR / "data"
SETTINGS_DIR = PROJECT_DIR / "settings"
MODULES_DIR = PROJECT_DIR / "modules"
CAPABILITIES_DIR = PROJECT_DIR / "capabilities"
SETTINGS_DIR = PROJECT_DIR / "settings"
MODEL_FILE = SETTINGS_DIR / "model.json"

# Файлы
HISTORY_FILE = DATA_DIR / "history.json"
LOG_FILE = DATA_DIR / "logs.txt"
# программы
PROGRAMS_FILE = CAPABILITIES_DIR / "programs.json"
USER_PROGRAMS_FILE = CAPABILITIES_DIR / "user_programs.json"
SCAN_SETTINGS_FILE = CAPABILITIES_DIR / "scan_settings.json"
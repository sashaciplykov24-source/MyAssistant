import ollama
from settings.config import SYSTEM_PROMPT
import json
from paths import MODEL_FILE

def load_model():

    with open(MODEL_FILE, "r", encoding="utf-8") as file:

        data = json.load(file)

    return data["model"]


def ask_ai(history):

    response = ollama.chat(
        model=load_model(),
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + history
    )

    return response["message"]["content"]

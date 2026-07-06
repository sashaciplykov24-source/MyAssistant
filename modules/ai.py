import ollama
from settings.config import SYSTEM_PROMPT
import json

def load_model():

    with open("settings/model.json", "r", encoding="utf-8") as file:

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
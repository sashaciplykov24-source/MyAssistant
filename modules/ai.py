import ollama
from settings.config import MODEL, SYSTEM_PROMPT


def ask_ai(history):

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ] + history
    )

    return response["message"]["content"]
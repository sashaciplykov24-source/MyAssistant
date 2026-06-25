import ollama

def get_models():

    models = ollama.list()

    result = []

    for model in models["models"]:
        result.append(model["name"])

    return result
models = get_models()

print("Доступные модели:")

for i, model in enumerate(models, start=1):
    print(f"{i}. {model}")

#for model in models["models"]:
#        if model["name"] == model_name:
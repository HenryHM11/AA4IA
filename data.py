import json

def cargar_datos():
    with open("data.json", "r") as file:
        data = json.load(file)
    return data

def guardar_datos(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=2)

def aprender_respuesta(usuario_key, Learning, data):
    respuesta_aprendida = input(f"Lo siento, no sé la respuesta. ¿Cuál debería ser la respuesta a '{usuario_key}'? ")
    Learning[usuario_key.lower()] = respuesta_aprendida
    guardar_datos(data)

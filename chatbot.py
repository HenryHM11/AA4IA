import difflib
import re
from data import cargar_datos, guardar_datos, aprender_respuesta

# Carga inicial de datos
data = cargar_datos()
Cuestions = data.get("Cuestions", {})
Cuestions_ban = data.get("Cuestions_ban", {})
Neuro = data.get("Neuro", {})
Learning = data.get("Learning", {})

def process_input(usuario_key):
    usuario_key = usuario_key.lower()
    if usuario_key in Learning:
        return Learning[usuario_key]

    mejor_mind = difflib.get_close_matches(usuario_key, Cuestions.keys())
    if mejor_mind:
        respuesta = Cuestions[mejor_mind[0]]
    else:
        respuesta = "No entiendo lo que estás diciendo. ¿Puedes reformular tu pregunta?"
    return respuesta

def process_input_neuro(usuario_key):
    usuario_key = usuario_key.lower()
    mejor_mind = difflib.get_close_matches(usuario_key, Neuro.keys())
    if mejor_mind:
        respuesta = Neuro[mejor_mind[0]]
        return respuesta
    return None

def process_input_ban(usuario_key):
    usuario_key = usuario_key.lower()
    for palabra_ban in Cuestions_ban:
        if palabra_ban in usuario_key:
            asteriscos = palabra_ban[0] + '*' * (len(palabra_ban)-1)
            respuesta = f"Lo siento, pero la palabra {asteriscos} incumple con nuestras normas al ser una expresión {Cuestions_ban[palabra_ban]}."
            return respuesta
    return None

def es_operacion_matematica(usuario_key):
    patron_operacion = re.compile(r'\b(\d+\s*[\+\-\*/]\s*\d+)\b')
    return bool(patron_operacion.search(usuario_key))

def obtener_respuesta(usuario_key):
    respuesta_ban = process_input_ban(usuario_key)

    if respuesta_ban:
        return respuesta_ban
    else:
        respuesta_neuro = process_input_neuro(usuario_key)
        if respuesta_neuro:
            return respuesta_neuro
        elif es_operacion_matematica(usuario_key):
            resultado = eval(usuario_key)
            return "El resultado es {}".format(resultado)
        else:
            respuesta = process_input(usuario_key)
            if respuesta == "No entiendo lo que estás diciendo. ¿Puedes reformular tu pregunta?":
                return "Enseñame: " + usuario_key
            else:
                return respuesta

def aprender_respuesta_web(usuario_key, respuesta_aprendida):
    Learning[usuario_key.lower()] = respuesta_aprendida
    guardar_datos(data)

if __name__ == "__main__":
    print("Chatbot: ¡Hola! Soy kiti un chatbot. Puedes escribir 'Bye' para salir.")

    while True:
        usuario_key = input("Tú: ")

        if usuario_key.lower() == "bye":
            # Guardar datos antes de salir
            data["Cuestions"] = Cuestions
            data["Cuestions_ban"] = Cuestions_ban
            data["Neuro"] = Neuro
            data["Learning"] = Learning
            guardar_datos(data)

            print("Chatbot: Bye te espero pronto!")
            break

        respuesta_ban = process_input_ban(usuario_key)

        if respuesta_ban:
            print("Chatbot: " + respuesta_ban)
        else:
            respuesta_neuro = process_input_neuro(usuario_key)
            if respuesta_neuro:
                resultado = respuesta_neuro
                print("Chatbot: " + resultado)
            elif es_operacion_matematica(usuario_key):
                resultado = eval(usuario_key)
                print("Chatbot: El resultado es {}".format(resultado))
            else:
                respuesta = process_input(usuario_key)
                if respuesta == "No entiendo lo que estás diciendo. ¿Puedes reformular tu pregunta?":
                    aprender_respuesta(usuario_key, Learning, data)
                else:
                    print("Chatbot: " + respuesta)

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from fila import contar_fichas_por_fila
from grupo import clasificar_circulos
from color import contar_circulos_por_color
#bot
from flask import Flask, render_template, request, jsonify
from chatbot import process_input, process_input_neuro, process_input_ban, es_operacion_matematica, Learning
from data import cargar_datos, guardar_datos
from flask import Flask, render_template, request, jsonify
from chatbot import obtener_respuesta, aprender_respuesta_web

import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'  
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():

    imagenes_disponibles = os.listdir(os.path.join('static', 'img'))

    return render_template('index.html', imagenes=imagenes_disponibles)

@app.route('/procesar', methods=['POST'])
def procesar_imagen():
    nombre_imagen = request.form['imagen']

    ruta_imagen = os.path.join('static', 'img', nombre_imagen)

    resultado_fila = contar_fichas_por_fila(ruta_imagen)
    resultado_grupo = clasificar_circulos(ruta_imagen)
    resultado_color = contar_circulos_por_color(ruta_imagen)

    return render_template('resultados.html', resultado_fila=resultado_fila, resultado_grupo=resultado_grupo, resultado_color=resultado_color)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/static/img/<filename>')
def serve_image(filename):
    return send_from_directory('static/img', filename)


#chatbot
@app.route('/', methods=['GET', 'POST'])
def indexbot():
    if request.method == 'POST':
        
        pass

    Cuestions, Cuestions_ban, Neuro, Learning = cargar_datos()
    return render_template('indexbot.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['user_message']
    bot_response = obtener_respuesta(user_message)
    return jsonify({'bot_response': bot_response})

@app.route('/teach_bot', methods=['POST'])
def teach_bot():
    user_message = request.form['user_message']
    respuesta_aprendida = request.form['respuesta_aprendida']
    aprender_respuesta_web(user_message, respuesta_aprendida)
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)

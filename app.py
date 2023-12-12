from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from fila import contar_fichas_por_fila
from grupo import clasificar_circulos
from color import contar_circulos_por_color
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'  # Carpeta donde se guardarán las imágenes procesadas
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Ruta principal para cargar la página con las imágenes
@app.route('/')
def index():
    # Listar las imágenes disponibles en la carpeta 'static/img'
    imagenes_disponibles = os.listdir(os.path.join('static', 'img'))

    return render_template('index.html', imagenes=imagenes_disponibles)

# Ruta para procesar la imagen seleccionada por el usuario
@app.route('/procesar', methods=['POST'])
def procesar_imagen():
    # Obtener el nombre de la imagen seleccionada por el usuario
    nombre_imagen = request.form['imagen']

    # Construir la ruta completa de la imagen
    ruta_imagen = os.path.join('static', 'img', nombre_imagen)

    # Procesar la imagen en cada módulo
    resultado_fila = contar_fichas_por_fila(ruta_imagen)
    resultado_grupo = clasificar_circulos(ruta_imagen)
    resultado_color = contar_circulos_por_color(ruta_imagen)

    # Mostrar la página de resultados con las imágenes procesadas
    return render_template('resultados.html', resultado_fila=resultado_fila, resultado_grupo=resultado_grupo, resultado_color=resultado_color)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)

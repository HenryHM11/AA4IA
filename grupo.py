import cv2
import numpy as np

def clasificar_circulos(imagen_path):
    # Cargar la imagen
    imagen = cv2.imread(imagen_path)

    # Convertir la imagen a escala de grises
    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Convertir la imagen a espacio de color HSV
    imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    # Definir rangos de color para amarillo y rojo en HSV
    rango_amarillo = [(20, 100, 100), (30, 255, 255)]  # Valores de H, S, V para amarillo
    rango_rojo1 = [(0, 100, 100), (10, 255, 255)]  # Valores de H, S, V para rojo
    rango_rojo2 = [(160, 100, 100), (180, 255, 255)]  # Valores de H, S, V para rojo

    # Filtrar la imagen para obtener las regiones de amarillo y rojo
    mascara_amarillo = cv2.inRange(imagen_hsv, rango_amarillo[0], rango_amarillo[1])
    mascara_rojo1 = cv2.inRange(imagen_hsv, rango_rojo1[0], rango_rojo1[1])
    mascara_rojo2 = cv2.inRange(imagen_hsv, rango_rojo2[0], rango_rojo2[1])

    # Combinar las máscaras de rojo
    mascara_rojo = cv2.bitwise_or(mascara_rojo1, mascara_rojo2)

    # Combinar las máscaras de amarillo y rojo
    mascara_color = cv2.bitwise_or(mascara_amarillo, mascara_rojo)

    # Aplicar un suavizado para reducir el ruido
    imagen_suavizada = cv2.medianBlur(imagen_gris, 5)

    # Aplicar la transformada de Hough para detectar círculos
    circulos = cv2.HoughCircles(
        imagen_suavizada,
        cv2.HOUGH_GRADIENT,
        dp=1,
        minDist=50,
        param1=60,
        param2=33,
        minRadius=20,
        maxRadius=100
    )

    # Inicializar listas para los círculos de cada grupo
    circulos_grupo1 = []
    circulos_grupo2 = []

    # Si se detectan círculos, clasificarlos en grupos
    if circulos is not None:
        circulos = np.uint16(np.around(circulos))
        for i in circulos[0, :]:
            x, y, r = i[0], i[1], i[2]

            # Verificar si el centro del círculo está en una región de color
            if y < imagen.shape[0] // 2:  # Mitad superior
                circulos_grupo1.append((x, y, r))  # Grupo 1
            else:
                circulos_grupo2.append((x, y, r))  # Grupo 2

    # Dibujar círculos alrededor de los grupos
    dibujar_grupo(imagen, circulos_grupo1, (0, 255, 0))  # Grupo 1 (color verde)
    dibujar_grupo(imagen, circulos_grupo2, (0, 0, 255))  # Grupo 2 (color rojo)

    # Imprimir la cantidad de círculos en cada grupo
    cantidad_grupo1 = len(circulos_grupo1)
    cantidad_grupo2 = len(circulos_grupo2)

    # Agregar el texto a la imagen
    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(imagen, f'Cantidad de circulos en Grupo 2: {cantidad_grupo2}', (10, imagen.shape[0] - 50), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
    cv2.putText(imagen, f'Cantidad de circulos en Grupo 1: {cantidad_grupo1}', (10, imagen.shape[0] - 20), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
    # Guardar la imagen resultante en el directorio 'uploads'
    ruta_guardado = 'uploads/resultado_grupo.jpg'
    cv2.imwrite(ruta_guardado, imagen)

    return ruta_guardado

def dibujar_grupo(imagen, circulos, color):
    for circulo in circulos:
        x, y, r = circulo
        cv2.circle(imagen, (x, y), r, color, 2)
        cv2.circle(imagen, (x, y), 5, color, -1)  # Centro del círculo

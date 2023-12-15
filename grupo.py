import cv2
import numpy as np

def clasificar_circulos(imagen_path):
    imagen = cv2.imread(imagen_path)

    imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    imagen_hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

    rango_amarillo = [(20, 100, 100), (30, 255, 255)]  
    rango_rojo1 = [(0, 100, 100), (10, 255, 255)]  
    rango_rojo2 = [(160, 100, 100), (180, 255, 255)]  

    mascara_amarillo = cv2.inRange(imagen_hsv, rango_amarillo[0], rango_amarillo[1])
    mascara_rojo1 = cv2.inRange(imagen_hsv, rango_rojo1[0], rango_rojo1[1])
    mascara_rojo2 = cv2.inRange(imagen_hsv, rango_rojo2[0], rango_rojo2[1])

    mascara_rojo = cv2.bitwise_or(mascara_rojo1, mascara_rojo2)

    mascara_color = cv2.bitwise_or(mascara_amarillo, mascara_rojo)

    imagen_suavizada = cv2.medianBlur(imagen_gris, 5)

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

    circulos_grupo1 = []
    circulos_grupo2 = []

    if circulos is not None:
        circulos = np.uint16(np.around(circulos))
        for i in circulos[0, :]:
            x, y, r = i[0], i[1], i[2]

            if y < imagen.shape[0] // 2:  
                circulos_grupo1.append((x, y, r))  
            else:
                circulos_grupo2.append((x, y, r)) 

    dibujar_grupo(imagen, circulos_grupo1, (0, 255, 0))  
    dibujar_grupo(imagen, circulos_grupo2, (0, 0, 255)) 

    cantidad_grupo1 = len(circulos_grupo1)
    cantidad_grupo2 = len(circulos_grupo2)

    font = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(imagen, f'Cantidad de circulos en Grupo 2: {cantidad_grupo2}', (10, imagen.shape[0] - 50), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
    cv2.putText(imagen, f'Cantidad de circulos en Grupo 1: {cantidad_grupo1}', (10, imagen.shape[0] - 20), font, 1.2, (0, 0, 255), 3, cv2.LINE_AA)
    ruta_guardado = 'uploads/resultado_grupo.jpg'
    cv2.imwrite(ruta_guardado, imagen)

    return ruta_guardado

def dibujar_grupo(imagen, circulos, color):
    for circulo in circulos:
        x, y, r = circulo
        cv2.circle(imagen, (x, y), r, color, 2)
        cv2.circle(imagen, (x, y), 5, color, -1)  
